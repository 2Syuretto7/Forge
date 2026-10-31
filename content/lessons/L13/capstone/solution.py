# %% [markdown]
# # L13 capstone: the same GPT in mixed precision
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. You will inspect the
# floating-point formats PyTorch offers, train the L10-style GPT twice from the same initial weights
# (once in fp32 and once with automatic mixed precision and loss scaling), and show that the losses
# match while the mixed-precision run is faster and uses less memory. The last cell is the
# autograder. (The T4 has no bf16 tensor cores, so on it mixed precision means fp16 with a gradient
# scaler; without a GPU the notebook uses bf16 autocast on the CPU.)

# %%
import copy
import hashlib
import math
import os
import pathlib
import time
import urllib.request

import torch
import torch.nn as nn
import torch.nn.functional as F

SMALL = os.environ.get("SMALL") == "1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
AMP_DTYPE = torch.float16 if DEVICE == "cuda" else torch.bfloat16
print("device:", torch.cuda.get_device_name(0) if DEVICE == "cuda" else "CPU", "| mixed precision in", AMP_DTYPE)

# %% [markdown]
# ## 1. The formats
#
# Fill in `format_info`: for a floating-point dtype, its total bits, its machine epsilon, its largest
# finite value and its smallest positive normal value, from `torch.finfo`.

# %%
def format_info(dtype):
    # BEGIN SOLUTION
    fi = torch.finfo(dtype)
    return {"bits": fi.bits, "eps": fi.eps, "max": fi.max, "tiny": fi.tiny}
    # END SOLUTION


for dt in (torch.float32, torch.bfloat16, torch.float16):
    print(dt, format_info(dt))

# %% [markdown]
# ## 2. Data and model
#
# Characters of Shakespeare as tokens, to keep the notebook self-contained, and the L10 model,
# large enough that matrix products dominate its time.

# %%
CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
CORPUS_SHA256 = "86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed"
local = [p for p in (pathlib.Path("data/tinyshakespeare.txt"), pathlib.Path("../data/tinyshakespeare.txt")) if p.exists()]
raw = local[0].read_bytes() if local else urllib.request.urlopen(CORPUS_URL, timeout=60).read()
assert hashlib.sha256(raw).hexdigest() == CORPUS_SHA256, "unexpected corpus contents"
text = raw.decode("utf-8")
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in text], dtype=torch.long)

CFG = dict(ctx=256, d=384, n_layer=6, n_head=6, batch=32, steps=300, lr=1e-3)
if SMALL:
    CFG.update(ctx=32, d=32, n_layer=1, n_head=2, batch=8, steps=30)


class Block(nn.Module):
    def __init__(self, d, n_head):
        super().__init__()
        self.n_head = n_head
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv, self.proj = nn.Linear(d, 3 * d), nn.Linear(d, d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def forward(self, x):
        B, T, d = x.shape
        q, k, v = self.qkv(self.ln1(x)).split(d, dim=2)
        q, k, v = (t.view(B, T, self.n_head, d // self.n_head).transpose(1, 2) for t in (q, k, v))
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        x = x + self.proj(y.transpose(1, 2).reshape(B, T, d))
        return x + self.mlp(self.ln2(x))


class GPT(nn.Module):
    def __init__(self, vocab, ctx, d, n_layer, n_head):
        super().__init__()
        self.tok, self.pos = nn.Embedding(vocab, d), nn.Embedding(ctx, d)
        nn.init.normal_(self.tok.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)
        self.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)

    def forward(self, idx):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device))
        for b in self.blocks:
            x = b(x)
        return self.ln_f(x) @ self.tok.weight.T


torch.manual_seed(0)
base_model = GPT(len(chars), CFG["ctx"], CFG["d"], CFG["n_layer"], CFG["n_head"])
print(f"{sum(p.numel() for p in base_model.parameters()) / 1e6:.1f}M parameters")


def batches(steps, seed=0):
    g = torch.Generator().manual_seed(seed)
    for _ in range(steps):
        ix = torch.randint(len(data) - CFG["ctx"] - 1, (CFG["batch"],), generator=g)
        x = torch.stack([data[i:i + CFG["ctx"]] for i in ix])
        y = torch.stack([data[i + 1:i + CFG["ctx"] + 1] for i in ix])
        yield x.to(DEVICE), y.to(DEVICE)


# %% [markdown]
# ## 3. Two training runs
#
# `train_fp32` is given. Write `train_amp`: the same loop with the forward pass and loss under
# `torch.autocast(device_type=..., dtype=AMP_DTYPE)`, and a `torch.amp.GradScaler` when the dtype is
# fp16 (it multiplies the loss before `backward`, unscales the gradients before clipping, skips steps
# with infinite gradients and adjusts its scale). Both functions return
# `(losses, seconds per step, peak memory in bytes)`.

# %%
def peak_reset():
    if DEVICE == "cuda":
        torch.cuda.synchronize()
        torch.cuda.reset_peak_memory_stats()


def peak_bytes():
    return torch.cuda.max_memory_allocated() if DEVICE == "cuda" else 0


def train_fp32(model):
    opt = torch.optim.AdamW(model.parameters(), lr=CFG["lr"], weight_decay=0.1)
    losses = []
    peak_reset()
    t0 = time.perf_counter()
    for x, y in batches(CFG["steps"]):
        loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
        losses.append(loss.detach())
    if DEVICE == "cuda":
        torch.cuda.synchronize()
    return [v.item() for v in losses], (time.perf_counter() - t0) / CFG["steps"], peak_bytes()


def train_amp(model):
    # BEGIN SOLUTION
    opt = torch.optim.AdamW(model.parameters(), lr=CFG["lr"], weight_decay=0.1)
    scaler = torch.amp.GradScaler(DEVICE, enabled=(AMP_DTYPE == torch.float16))
    losses = []
    peak_reset()
    t0 = time.perf_counter()
    for x, y in batches(CFG["steps"]):
        with torch.autocast(device_type=DEVICE, dtype=AMP_DTYPE):
            loss = F.cross_entropy(model(x).flatten(0, 1).float(), y.flatten())
        opt.zero_grad(set_to_none=True)
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(opt)
        scaler.update()
        losses.append(loss.detach())
    if DEVICE == "cuda":
        torch.cuda.synchronize()
    train_amp.final_scale = scaler.get_scale() if scaler.is_enabled() else 1.0
    return [v.item() for v in losses], (time.perf_counter() - t0) / CFG["steps"], peak_bytes()
    # END SOLUTION


fp32_losses, fp32_time, fp32_mem = train_fp32(copy.deepcopy(base_model).to(DEVICE))
amp_losses, amp_time, amp_mem = train_amp(copy.deepcopy(base_model).to(DEVICE))
speedup = fp32_time / amp_time
tail = max(1, CFG["steps"] // 10)
fp32_final = sum(fp32_losses[-tail:]) / tail
amp_final = sum(amp_losses[-tail:]) / tail
print(f"fp32: {fp32_time * 1e3:.1f} ms/step, final loss {fp32_final:.4f}, peak {fp32_mem / 1e6:.0f} MB")
print(f"amp:  {amp_time * 1e3:.1f} ms/step, final loss {amp_final:.4f}, peak {amp_mem / 1e6:.0f} MB")
print(f"speedup {speedup:.2f}x")

# %% [markdown]
# ## 4. Report
#
# At least 80 words: the formats you used and why (range, precision, hardware), the measured speedup
# and memory, how closely the losses agree, and what the gradient scaler did.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
REPORT = f"""
The fp32 run keeps every tensor in single precision; the mixed-precision run computes the matrix
products and most activations in {AMP_DTYPE} under autocast while the parameters, the optimizer state
and the reductions (softmax, layer norm, the loss) stay in fp32. On the T4 the format is fp16, whose
tensor cores multiply eight times faster than its fp32 units, and whose narrow range needs a gradient
scaler: it multiplies the loss so that small gradients do not underflow, skips any step whose gradients
overflow, and adjusts the scale. Here the mixed-precision step took {amp_time * 1e3:.1f} ms against
{fp32_time * 1e3:.1f} ms, a speedup of {speedup:.2f}, with peak memory {amp_mem / 1e6:.0f} MB against
{fp32_mem / 1e6:.0f} MB, and the final losses were {amp_final:.4f} and {fp32_final:.4f}.
"""
# END SOLUTION
