# %% [markdown]
# # L09 capstone: a transformer that writes like Shakespeare (badly)
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. You will write
# causal multi-head self-attention, a pre-norm decoder block and a small GPT in PyTorch, check them
# against PyTorch's own attention, and train a two-layer model on about a megabyte of Shakespeare,
# character by character, to a validation loss below 1.70 nats per character. The last cell is the
# autograder; it prints a completion code to paste into the lesson.

# %%
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
torch.manual_seed(0)
print("device:", torch.cuda.get_device_name(0) if DEVICE == "cuda" else "CPU")

# %% [markdown]
# ## 1. The corpus
#
# About 1.1 MB of Shakespeare's plays (public domain), the "tiny Shakespeare" file compiled for the
# char-rnn project. The hash check makes sure everyone trains on exactly the same text.

# %%
CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
CORPUS_SHA256 = "86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed"
# Inside a checkout of the Forge repository the file is already there; in Colab it is downloaded.
local = [p for p in (pathlib.Path("data/tinyshakespeare.txt"), pathlib.Path("../data/tinyshakespeare.txt")) if p.exists()]
raw = local[0].read_bytes() if local else urllib.request.urlopen(CORPUS_URL, timeout=60).read()
assert hashlib.sha256(raw).hexdigest() == CORPUS_SHA256, "unexpected corpus contents"
text = raw.decode("utf-8")
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
VOCAB = len(chars)
data = torch.tensor([stoi[c] for c in text], dtype=torch.long)
split = int(0.9 * len(data))
train_data, val_data = data[:split], data[split:]
print(f"{len(text):,} characters, vocabulary of {VOCAB}")


def get_batch(src, batch, ctx, gen):
    ix = torch.randint(len(src) - ctx - 1, (batch,), generator=gen)
    x = torch.stack([src[i:i + ctx] for i in ix])
    y = torch.stack([src[i + 1:i + ctx + 1] for i in ix])
    return x.to(DEVICE), y.to(DEVICE)


# %% [markdown]
# ## 2. Causal multi-head self-attention
#
# Write the forward pass yourself: project to queries, keys and values with one linear layer, split
# into heads, compute the scaled scores, mask the future, softmax, weight the values, merge the heads
# and project. Do not call `F.scaled_dot_product_attention`; the test compares your result with it.

# %%
class CausalSelfAttention(nn.Module):
    def __init__(self, d, n_head):
        super().__init__()
        assert d % n_head == 0
        self.n_head = n_head
        self.qkv = nn.Linear(d, 3 * d)
        self.proj = nn.Linear(d, d)

    def forward(self, x):
        B, T, d = x.shape
        # BEGIN SOLUTION
        q, k, v = self.qkv(x).split(d, dim=2)
        q, k, v = (t.view(B, T, self.n_head, d // self.n_head).transpose(1, 2) for t in (q, k, v))
        att = (q @ k.transpose(-2, -1)) / math.sqrt(d // self.n_head)
        mask = torch.triu(torch.ones(T, T, dtype=torch.bool, device=x.device), diagonal=1)
        att = att.masked_fill(mask, float("-inf")).softmax(dim=-1)
        y = (att @ v).transpose(1, 2).reshape(B, T, d)
        return self.proj(y)
        # END SOLUTION


def reference_attention(module, x):
    """The same computation with PyTorch's fused attention, for checking."""
    B, T, d = x.shape
    q, k, v = module.qkv(x).split(d, dim=2)
    q, k, v = (t.view(B, T, module.n_head, d // module.n_head).transpose(1, 2) for t in (q, k, v))
    y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
    return module.proj(y.transpose(1, 2).reshape(B, T, d))


# %% [markdown]
# ## 3. The decoder block and the model
#
# A pre-norm block (L06): `x + attn(ln1(x))`, then `x + mlp(ln2(x))` with a GELU MLP four times as
# wide. The model adds learned token and position embeddings, runs the blocks, applies a final layer
# norm and maps to vocabulary logits.

# %%
class Block(nn.Module):
    def __init__(self, d, n_head):
        super().__init__()
        self.ln1 = nn.LayerNorm(d)
        self.attn = CausalSelfAttention(d, n_head)
        self.ln2 = nn.LayerNorm(d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def forward(self, x):
        # BEGIN SOLUTION
        x = x + self.attn(self.ln1(x))
        return x + self.mlp(self.ln2(x))
        # END SOLUTION


class GPT(nn.Module):
    def __init__(self, vocab, ctx, d, n_layer, n_head):
        super().__init__()
        self.ctx = ctx
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(ctx, d)
        self.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)
        self.head = nn.Linear(d, vocab)

    def forward(self, idx):
        # BEGIN SOLUTION
        T = idx.shape[1]
        x = self.tok(idx) + self.pos(torch.arange(T, device=idx.device))
        for block in self.blocks:
            x = block(x)
        return self.head(self.ln_f(x))
        # END SOLUTION


def param_formula(vocab, ctx, d, n_layer):
    """Parameters of this GPT: embeddings, n_layer blocks, final norm and an untied output layer."""
    # BEGIN SOLUTION
    block = (3 * d * d + 3 * d) + (d * d + d) + 2 * d + (4 * d * d + 4 * d) + (4 * d * d + d) + 2 * d
    return vocab * d + ctx * d + n_layer * block + 2 * d + d * vocab + vocab
    # END SOLUTION


# %% [markdown]
# ## 4. Training
#
# The reference settings below reach the target on a T4 in about a minute. You may change them.

# %%
CFG = dict(ctx=128, d=128, n_layer=2, n_head=4, batch=64, steps=2000, lr=3e-3)
if SMALL:
    CFG.update(ctx=32, d=32, steps=60, batch=16)

model = GPT(VOCAB, CFG["ctx"], CFG["d"], CFG["n_layer"], CFG["n_head"]).to(DEVICE)
opt = torch.optim.AdamW(model.parameters(), lr=CFG["lr"], weight_decay=0.1)
gen = torch.Generator().manual_seed(0)
losses = []
t0 = time.time()
for step in range(1, CFG["steps"] + 1):
    lr = CFG["lr"] * min(1.0, step / 100) * 0.5 * (1.0 + math.cos(math.pi * step / CFG["steps"]))
    for group in opt.param_groups:
        group["lr"] = lr
    x, y = get_batch(train_data, CFG["batch"], CFG["ctx"], gen)
    loss = F.cross_entropy(model(x).view(-1, VOCAB), y.view(-1))
    opt.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    if step == 1 or step % max(1, CFG["steps"] // 20) == 0:
        losses.append((step, loss.item()))  # an occasional .item() is fine; every step would stall the GPU (L07)
    if step % 500 == 0:
        print(f"step {step}: train loss {loss.item():.3f} ({time.time() - t0:.0f} s)")


@torch.no_grad()
def estimate_loss(src, batches=20, seed=1):
    model.eval()
    g = torch.Generator().manual_seed(seed)
    total = 0.0
    for _ in range(batches):
        x, y = get_batch(src, CFG["batch"], CFG["ctx"], g)
        total += F.cross_entropy(model(x).view(-1, VOCAB), y.view(-1)).item()
    model.train()
    return total / batches


val_loss = estimate_loss(val_data)
print(f"validation loss: {val_loss:.3f} nats per character")

# %% [markdown]
# ## 5. Sampling
#
# Generate text one character at a time, feeding the model its own output (at most `ctx` characters
# of context), sampling from the softmax at temperature 0.8.

# %%
@torch.no_grad()
def sample(n_chars, prompt="ROMEO:\n", temperature=0.8, seed=0):
    model.eval()
    g = torch.Generator(device=DEVICE).manual_seed(seed)
    idx = torch.tensor([[stoi[c] for c in prompt]], device=DEVICE)
    for _ in range(n_chars):
        logits = model(idx[:, -CFG["ctx"]:])[:, -1, :] / temperature
        nxt = torch.multinomial(logits.softmax(dim=-1), 1, generator=g)
        idx = torch.cat([idx, nxt], dim=1)
    model.train()
    return "".join(chars[i] for i in idx[0].tolist())


sample_text = sample(300)
print(sample_text)
