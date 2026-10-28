"""Writes src/widgets/data/spike_runs.json, the logged training runs the LossSpikeExplorer widget
replays. Every run trains the same small character-level GPT on Tiny Shakespeare on a CPU, from the
same initialization and with the same sequence of batches, so runs differ only in what each one
changes. One value per optimizer step: the batch loss, the gradient norm before clipping, the
learning rate and the largest attention logit, plus the validation loss every 100 steps.

Run from the repository root with PyTorch installed (about 15 minutes on four CPU cores):
    python scripts/gen_spike_runs.py
"""
import json
import math
import os

import torch
import torch.nn as nn
import torch.nn.functional as F

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, "src", "widgets", "data", "spike_runs.json")
STEPS, CTX, BATCH, D, LAYERS, HEADS = 1200, 128, 32, 128, 4, 4
CHECKPOINT_EVERY = 100
BAD = range(700, 710)  # the corrupted stretch of data
torch.set_num_threads(4)

text = open(os.path.join(ROOT, "data", "tinyshakespeare.txt")).read()
chars = sorted(set(text))
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in text])
split = int(0.9 * len(data))
train, val = data[:split], data[split:]


class Block(nn.Module):
    def __init__(self, qk_norm):
        super().__init__()
        self.ln1, self.ln2 = nn.LayerNorm(D), nn.LayerNorm(D)
        self.qkv, self.proj = nn.Linear(D, 3 * D), nn.Linear(D, D)
        self.mlp = nn.Sequential(nn.Linear(D, 4 * D), nn.GELU(), nn.Linear(4 * D, D))
        self.qn = nn.LayerNorm(D // HEADS) if qk_norm else nn.Identity()
        self.kn = nn.LayerNorm(D // HEADS) if qk_norm else nn.Identity()
        self.max_logit = 0.0

    def forward(self, x):
        B, T, _ = x.shape
        q, k, v = self.qkv(self.ln1(x)).split(D, 2)
        q, k, v = (t.view(B, T, HEADS, D // HEADS).transpose(1, 2) for t in (q, k, v))
        q, k = self.qn(q), self.kn(k)
        att = q @ k.transpose(-1, -2) / math.sqrt(D // HEADS)
        mask = torch.ones(T, T, dtype=torch.bool).triu(1)
        self.max_logit = att.detach().masked_fill(mask, 0).abs().max().item()
        att = att.masked_fill(mask, float("-inf")).softmax(-1)
        x = x + self.proj((att @ v).transpose(1, 2).reshape(B, T, D))
        return x + self.mlp(self.ln2(x))


class GPT(nn.Module):
    def __init__(self, qk_norm):
        super().__init__()
        self.tok, self.pos = nn.Embedding(len(chars), D), nn.Embedding(CTX, D)
        nn.init.normal_(self.tok.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)
        self.blocks = nn.ModuleList([Block(qk_norm) for _ in range(LAYERS)])
        self.ln_f = nn.LayerNorm(D)

    def forward(self, idx):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1]))
        for b in self.blocks:
            x = b(x)
        return self.ln_f(x) @ self.tok.weight.T


@torch.no_grad()
def val_loss(model):
    model.eval()
    g = torch.Generator().manual_seed(1)
    total = 0.0
    for _ in range(10):
        ix = torch.randint(len(val) - CTX - 1, (64,), generator=g)
        x = torch.stack([val[i:i + CTX] for i in ix])
        y = torch.stack([val[i + 1:i + CTX + 1] for i in ix])
        total += F.cross_entropy(model(x).flatten(0, 1), y.flatten()).item()
    model.train()
    return total / 10


def run(lr=3e-3, warmup=100, clip=1.0, qk_norm=False, bad_data=False, lr_bug=False):
    torch.manual_seed(0)
    model = GPT(qk_norm)
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    order = torch.Generator().manual_seed(0)
    noise = torch.Generator().manual_seed(123)
    log = {"loss": [], "gradNorm": [], "lr": [], "maxLogit": [], "val": []}
    for step in range(1, STEPS + 1):
        cur = lr * min(1.0, step / warmup) if warmup else lr
        cur *= 0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * step / STEPS))
        if lr_bug and 700 <= step < 760:
            cur *= 20  # a schedule bug: the learning rate is multiplied instead of divided
        for group in opt.param_groups:
            group["lr"] = cur
        ix = torch.randint(len(train) - CTX - 1, (BATCH,), generator=order)
        x = torch.stack([train[i:i + CTX] for i in ix])
        y = torch.stack([train[i + 1:i + CTX + 1] for i in ix])
        if bad_data and step in BAD:
            # A shard of binary junk decoded as text: uniformly random characters.
            x = torch.randint(len(chars), x.shape, generator=noise)
            y = torch.randint(len(chars), y.shape, generator=noise)
        loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
        opt.zero_grad(set_to_none=True)
        loss.backward()
        norm = torch.nn.utils.clip_grad_norm_(model.parameters(), clip if clip else float("inf")).item()
        opt.step()
        log["loss"].append(float(f"{loss.item():.4g}"))
        log["gradNorm"].append(float(f"{norm:.4g}"))
        log["lr"].append(float(f"{cur:.4g}"))
        log["maxLogit"].append(float(f"{max(b.max_logit for b in model.blocks):.4g}"))
        if step % CHECKPOINT_EVERY == 0:
            log["val"].append([step, round(val_loss(model), 4)])
        if not math.isfinite(loss.item()):
            break
    return log


RUNS = {
    "healthy": dict(
        label="healthy",
        note="Peak learning rate 3e-3 after 100 warmup steps, cosine decay, gradients clipped at norm 1.",
        config=dict(),
    ),
    "bad_data": dict(
        label="bad data, clipped",
        note="Steps 700 to 709 train on random characters: a corrupted shard. Clipping limits each update.",
        config=dict(bad_data=True),
    ),
    "bad_data_noclip": dict(
        label="bad data, no clipping",
        note="The same corrupted shard without gradient clipping.",
        config=dict(bad_data=True, clip=None),
    ),
    "lr_bug": dict(
        label="learning-rate bug",
        note="For steps 700 to 759 a schedule bug multiplies the learning rate by 20.",
        config=dict(lr_bug=True),
    ),
    "high_lr": dict(
        label="lr 1e-2, no warmup",
        note="Peak learning rate 1e-2 from the first step, no warmup, no clipping.",
        config=dict(lr=1e-2, warmup=0, clip=None),
    ),
    "high_lr_qknorm": dict(
        label="lr 1e-2, no warmup, QK-layernorm",
        note="As before, with a layer norm on each head's queries and keys.",
        config=dict(lr=1e-2, warmup=0, clip=None, qk_norm=True),
    ),
}

if __name__ == "__main__":
    runs = {}
    for name, spec in RUNS.items():
        runs[name] = {"label": spec["label"], "note": spec["note"], **run(**spec["config"])}
        last = runs[name]["val"][-1] if runs[name]["val"] else None
        print(name, "steps", len(runs[name]["loss"]), "final validation", last, flush=True)
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    meta = f"A character-level GPT ({LAYERS} layers, d = {D}, {HEADS} heads, context {CTX}, batch {BATCH}) on Tiny Shakespeare, AdamW."
    with open(OUT, "w") as f:
        json.dump({"model": meta, "checkpointEvery": CHECKPOINT_EVERY, "runs": runs}, f, separators=(",", ":"))
        f.write("\n")
    print("wrote", os.path.relpath(OUT, ROOT))
