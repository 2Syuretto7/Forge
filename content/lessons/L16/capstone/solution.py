# %% [markdown]
# # L16 capstone: teach a pretrained model two tasks without making it forget
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. The notebook
# pretrains a small byte-level GPT on Tiny Shakespeare for a few minutes, so there is a base model
# that knows English spelling but follows no instructions. You then teach it two tasks, writing a
# word in capitals and spelling it backwards, from instruction examples: with LoRA adapters, and
# with full fine-tuning for comparison. Each is scored on words it never saw in training, with a
# bootstrap interval, and on how much its loss on ordinary text rose. The last cell is the
# autograder; it prints a completion code to paste into the lesson.

# %%
import copy
import hashlib
import math
import os
import pathlib
import re
import time
import urllib.request

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

SMALL = os.environ.get("SMALL") == "1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", torch.cuda.get_device_name(0) if DEVICE == "cuda" else "CPU")

# %% [markdown]
# ## 1. Configuration and targets
#
# The LoRA model must reach `accuracy` exact-match accuracy on unseen words, averaged over both
# tasks, while its loss on held-out Shakespeare rises by at most `forgetting` nats per byte. Both
# methods replay pretraining text during fine-tuning: each step adds `replay` times the language
# modeling loss on `replay_batch` windows of Shakespeare. Without it, either method forgets most of
# what pretraining taught (set `replay=0` to see).

# %%
CFG = dict(d=192, n_layer=4, n_head=6, ctx=128, batch=32, pre_steps=2000, pre_lr=3e-3, sft_steps=1500,
           rank=16, alpha=32, lora_lr=2e-3, full_lr=3e-4, replay=2.0, replay_batch=8, n_test=300, seed=0)
TARGETS = dict(accuracy=0.8, forgetting=0.05)
if SMALL:
    CFG.update(d=48, n_layer=2, n_head=2, pre_steps=40, sft_steps=20, n_test=20)

CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
CORPUS_SHA256 = "86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed"
local = [p for p in (pathlib.Path("data/tinyshakespeare.txt"), pathlib.Path("../data/tinyshakespeare.txt")) if p.exists()]
raw_bytes = local[0].read_bytes() if local else urllib.request.urlopen(CORPUS_URL, timeout=60).read()
assert hashlib.sha256(raw_bytes).hexdigest() == CORPUS_SHA256, "unexpected corpus contents"
text = raw_bytes.decode("utf-8")
data = torch.tensor(list(raw_bytes), dtype=torch.long)
split = int(0.9 * len(data))
train_data, val_data = data[:split], data[split:]

# %% [markdown]
# ## 2. The base model
#
# The GPT of L10 at byte level, pretrained for a few minutes. `base_loss` is its loss on fixed
# windows of held-out text: the yardstick for forgetting.

# %%
class Block(nn.Module):
    def __init__(self, d, n_head):
        super().__init__()
        self.d, self.n_head = d, n_head
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv, self.proj = nn.Linear(d, 3 * d), nn.Linear(d, d)
        self.fc1, self.fc2 = nn.Linear(d, 4 * d), nn.Linear(4 * d, d)

    def forward(self, x):
        B, T, d = x.shape
        q, k, v = (t.view(B, T, self.n_head, d // self.n_head).transpose(1, 2) for t in self.qkv(self.ln1(x)).split(d, dim=2))
        x = x + self.proj(F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, d))
        return x + self.fc2(F.gelu(self.fc1(self.ln2(x))))


class GPT(nn.Module):
    def __init__(self, d, n_layer, n_head, ctx):
        super().__init__()
        self.tok, self.pos = nn.Embedding(256, d), nn.Embedding(ctx, d)
        nn.init.normal_(self.tok.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)
        self.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)

    def forward(self, idx):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device))
        for b in self.blocks:
            x = b(x)
        return self.ln_f(x) @ self.tok.weight.T


def windows(src, gen, n):
    ix = torch.randint(len(src) - CFG["ctx"] - 1, (n,), generator=gen)
    x = torch.stack([src[i:i + CFG["ctx"]] for i in ix])
    y = torch.stack([src[i + 1:i + CFG["ctx"] + 1] for i in ix])
    return x.to(DEVICE), y.to(DEVICE)


@torch.no_grad()
def base_loss(model, n=128):
    model.eval()
    x, y = windows(val_data, torch.Generator().manual_seed(1), n)
    loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten()).item()
    model.train()
    return loss


torch.manual_seed(CFG["seed"])
base = GPT(CFG["d"], CFG["n_layer"], CFG["n_head"], CFG["ctx"]).to(DEVICE)
opt = torch.optim.AdamW(base.parameters(), lr=CFG["pre_lr"], betas=(0.9, 0.95), weight_decay=0.1)
gen = torch.Generator().manual_seed(0)
t0 = time.time()
for step in range(1, CFG["pre_steps"] + 1):
    lr = CFG["pre_lr"] * min(1.0, step / 100) * (0.1 + 0.45 * (1 + math.cos(math.pi * step / CFG["pre_steps"])))
    for group in opt.param_groups:
        group["lr"] = lr
    x, y = windows(train_data, gen, CFG["batch"])
    loss = F.cross_entropy(base(x).flatten(0, 1), y.flatten())
    opt.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(base.parameters(), 1.0)
    opt.step()
    if step % 500 == 0 or step == CFG["pre_steps"]:
        print(f"pretraining step {step}: loss {loss.item():.3f} ({time.time() - t0:.0f} s)")
pre_loss = base_loss(base)
print(f"base model: {sum(p.numel() for p in base.parameters()):,} parameters, held-out loss {pre_loss:.4f} nats per byte")

# %% [markdown]
# ## 3. Instruction data
#
# Two tasks on words from the plays: `UPPER: word\n=` answered by the word in capitals, and
# `REVERSE: word\n=` answered by the word spelled backwards, each answer ending with a newline.
# The words are split once, before any training, into training words and test words.
#
# Write `encode_example(task, word)`: the bytes of prompt and answer joined, and a mask with 0 on
# every prompt byte and 1 on every answer byte (including the final newline, so the model learns to
# stop).

# %%
TASKS = {"UPPER": lambda w: w.upper(), "REVERSE": lambda w: w[::-1]}
words = sorted({w for w in re.findall(r"[a-z]+", text.lower()) if 3 <= len(w) <= 8})
rng = np.random.default_rng(CFG["seed"])
rng.shuffle(words)
test_words, train_words = words[:CFG["n_test"]], words[CFG["n_test"]:]
assert not set(test_words) & set(train_words)


def prompt_of(task, word):
    return f"{task}: {word}\n="


def answer_of(task, word):
    return TASKS[task](word) + "\n"


def encode_example(task, word):
    # BEGIN SOLUTION
    p, a = prompt_of(task, word).encode(), answer_of(task, word).encode()
    return list(p) + list(a), [0] * len(p) + [1] * len(a)
    # END SOLUTION


def sft_batch(n, gen):
    """Inputs, targets and the mask on the targets, padded with newlines that the mask ignores."""
    xs, ys, ms = [], [], []
    for _ in range(n):
        task = list(TASKS)[int(gen.integers(len(TASKS)))]
        ids, mask = encode_example(task, train_words[int(gen.integers(len(train_words)))])
        pad = CFG["ctx"] + 1 - len(ids)
        ids, mask = ids + [10] * pad, mask + [0] * pad
        xs.append(ids[:-1])
        ys.append(ids[1:])
        ms.append(mask[1:])
    return torch.tensor(xs).to(DEVICE), torch.tensor(ys).to(DEVICE), torch.tensor(ms, dtype=torch.float).to(DEVICE)


print(encode_example("REVERSE", "crown"))

# %% [markdown]
# ## 4. The loss and the adapters
#
# Write `masked_loss(logits, y, mask)`, the mean cross-entropy over the positions where the mask is
# 1. Then write `LoRALinear.forward`, the frozen layer plus $(\alpha / r)\, x A^\top B^\top$, and
# `merge`, which returns a plain `nn.Linear` with the update folded into its weight.
# `add_lora` wraps the four linear layers of every block and freezes everything else.

# %%
def masked_loss(logits, y, mask):
    # BEGIN SOLUTION
    per = F.cross_entropy(logits.flatten(0, 1), y.flatten(), reduction="none")
    return (per * mask.flatten()).sum() / mask.sum()
    # END SOLUTION


class LoRALinear(nn.Module):
    def __init__(self, base_layer, r, alpha):
        super().__init__()
        self.base, self.r, self.alpha = base_layer, r, alpha
        self.A = nn.Parameter(torch.randn(r, base_layer.in_features, device=base_layer.weight.device) / math.sqrt(base_layer.in_features))
        self.B = nn.Parameter(torch.zeros(base_layer.out_features, r, device=base_layer.weight.device))

    def forward(self, x):
        # BEGIN SOLUTION
        return self.base(x) + (self.alpha / self.r) * (x @ self.A.T) @ self.B.T
        # END SOLUTION

    def merge(self):
        # BEGIN SOLUTION
        layer = copy.deepcopy(self.base)
        layer.weight.data += (self.alpha / self.r) * self.B.data @ self.A.data
        return layer
        # END SOLUTION


LINEARS = ["qkv", "proj", "fc1", "fc2"]


def add_lora(model, r, alpha):
    for p in model.parameters():
        p.requires_grad_(False)
    for b in model.blocks:
        for name in LINEARS:
            setattr(b, name, LoRALinear(getattr(b, name), r, alpha))
    return model


def merge_lora(model):
    merged = copy.deepcopy(model)
    for b in merged.blocks:
        for name in LINEARS:
            layer = getattr(b, name)
            if isinstance(layer, LoRALinear):
                setattr(b, name, layer.merge())
    return merged


# %% [markdown]
# ## 5. Fine-tune and evaluate
#
# `finetune` trains a copy of the base model, with adapters or with every weight, on the same
# batches. `evaluate` decodes greedily on the test words and scores exact matches, with a bootstrap
# interval over words for each task.

# %%
def finetune(kind):
    model = copy.deepcopy(base)
    if kind == "lora":
        add_lora(model, CFG["rank"], CFG["alpha"])
        lr = CFG["lora_lr"]
    else:
        lr = CFG["full_lr"]
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=lr, weight_decay=0.0)
    gen = np.random.default_rng(1)
    replay_gen = torch.Generator().manual_seed(2)
    model.train()
    for step in range(1, CFG["sft_steps"] + 1):
        for group in opt.param_groups:
            group["lr"] = lr * min(1.0, step / 50)
        x, y, m = sft_batch(CFG["batch"], gen)
        loss = masked_loss(model(x), y, m)
        if CFG["replay"]:
            xr, yr = windows(train_data, replay_gen, CFG["replay_batch"])
            loss = loss + CFG["replay"] * F.cross_entropy(model(xr).flatten(0, 1), yr.flatten())
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(params, 1.0)
        opt.step()
    model.eval()
    return model, sum(p.numel() for p in params)


@torch.no_grad()
def generate(model, task, word, max_new=12):
    ids = torch.tensor([list(prompt_of(task, word).encode())], device=DEVICE)
    out = []
    for _ in range(max_new):
        nxt = int(model(ids)[0, -1].argmax())
        out.append(nxt)
        if nxt == 10:
            break
        ids = torch.cat([ids, torch.tensor([[nxt]], device=DEVICE)], dim=1)
    return bytes(out).decode("utf-8", errors="replace")


def evaluate(model, n_boot=2000):
    result = {}
    for task in TASKS:
        correct = np.array([generate(model, task, w) == answer_of(task, w) for w in test_words], dtype=float)
        means = correct[np.random.default_rng(0).integers(0, len(correct), (n_boot, len(correct)))].mean(axis=1)
        result[task] = (float(correct.mean()), *np.quantile(means, [0.025, 0.975]).tolist())
    result["mean"] = float(np.mean([result[t][0] for t in TASKS]))
    return result


results = {}
for kind in ["lora", "full"]:
    t0 = time.time()
    model, n_trainable = finetune(kind)
    results[kind] = dict(eval=evaluate(model), loss=base_loss(model), trainable=n_trainable, model=model)
    r = results[kind]
    print(f"{kind}: {n_trainable:,} trainable parameters, accuracy "
          + ", ".join(f"{t} {r['eval'][t][0]:.2f} [{r['eval'][t][1]:.2f}, {r['eval'][t][2]:.2f}]" for t in TASKS)
          + f", held-out loss {r['loss']:.4f} (+{r['loss'] - pre_loss:.4f}) ({time.time() - t0:.0f} s)")
base_eval = evaluate(base)
print(f"base model accuracy: UPPER {base_eval['UPPER'][0]:.2f}, REVERSE {base_eval['REVERSE'][0]:.2f}")

lora_model = results["lora"]["model"]
merged = merge_lora(lora_model)
x_check, _ = windows(val_data, torch.Generator().manual_seed(5), 4)
with torch.no_grad():
    merge_error = (merged(x_check) - lora_model(x_check)).abs().max().item()
print(f"merged model matches the adapted one to {merge_error:.1e}")
for task in TASKS:
    for w in test_words[:3]:
        print(f"{task}: {w} -> {generate(merged, task, w)!r}")

lora_accuracy = results["lora"]["eval"]["mean"]
lora_forgetting = results["lora"]["loss"] - pre_loss
full_forgetting = results["full"]["loss"] - pre_loss

# %% [markdown]
# ## 6. Report
#
# In `REPORT`, write at least 80 words: the accuracy of each method on each task with intervals,
# the forgetting of each, the number of trainable parameters, which method you would ship and
# why, and why the second task is harder for a model that reads one byte at a time.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
L, F_ = results["lora"], results["full"]
less = "LoRA" if lora_forgetting < full_forgetting else "full fine-tuning"
met = lora_accuracy >= TARGETS["accuracy"] and lora_forgetting <= TARGETS["forgetting"]
harder = min(TASKS, key=lambda t: L["eval"][t][0])
REPORT = f"""Fine-tuning report. The base model ({sum(p.numel() for p in base.parameters()):,} parameters, held-out loss {pre_loss:.3f} nats per
byte) could do neither task (UPPER {base_eval['UPPER'][0]:.2f}, REVERSE {base_eval['REVERSE'][0]:.2f}). After {CFG['sft_steps']} steps on the same
masked instruction batches, each with replayed Shakespeare at weight {CFG['replay']}, LoRA of rank {CFG['rank']} on every linear layer
({L['trainable']:,} trainable parameters) reached UPPER {L['eval']['UPPER'][0]:.2f} [{L['eval']['UPPER'][1]:.2f}, {L['eval']['UPPER'][2]:.2f}] and
REVERSE {L['eval']['REVERSE'][0]:.2f} [{L['eval']['REVERSE'][1]:.2f}, {L['eval']['REVERSE'][2]:.2f}] on {len(test_words)} unseen words, with forgetting of
{lora_forgetting:+.4f} nats per byte. Full fine-tuning ({F_['trainable']:,} parameters) reached UPPER {F_['eval']['UPPER'][0]:.2f} and
REVERSE {F_['eval']['REVERSE'][0]:.2f}, with forgetting of {full_forgetting:+.4f}; by this measure {less} disturbed the base model less. The
LoRA model {'meets' if met else 'misses'} the targets of {TARGETS['accuracy']:.0%} accuracy and {TARGETS['forgetting']} nats of forgetting. I would ship it merged
into the base weights: no inference cost, and the adapter alone is {L['trainable'] * 4 / 1e6:.1f} MB to store per task, against
{F_['trainable'] * 4 / 1e6:.1f} MB for a fully fine-tuned copy. {harder} was the harder task for LoRA; replaying pretraining text was
what kept forgetting small, since without it the fine-tuning loss alone pulls every weight toward the new format."""
# END SOLUTION
print(REPORT)
