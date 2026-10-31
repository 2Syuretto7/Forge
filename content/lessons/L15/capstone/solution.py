# %% [markdown]
# # L15 capstone: a pretraining run that survives its own failures
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. You will write the
# parts of a real training script: a learning-rate schedule that depends only on the step,
# checkpoints that capture everything needed to resume exactly, deterministic data positions, a
# spike detector with rollback, and an evaluation harness with error bars. Then you run the
# nanoGPT-sized character model (6 layers, width 384, about 10.7 million parameters) on Tiny
# Shakespeare for 5,000 steps, with a stretch of corrupted data injected at step 3,000, and write
# the run report. The last cell is the autograder; it prints a completion code to paste into the
# lesson.
#
# Checkpoints go to Google Drive if it is mounted (`from google.colab import drive;
# drive.mount('/content/drive')`), so a disconnected session can resume where it stopped; otherwise
# to a temporary folder.

# %%
import hashlib
import json
import math
import os
import pathlib
import tempfile
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
# ## 1. Configuration
#
# One dictionary holds every setting; it is saved in every checkpoint and in the report. The data
# positions in `BAD` will be replaced by random characters, a corrupted shard.

# %%
CFG = dict(d=384, n_layer=6, n_head=6, ctx=256, batch=32, dropout=0.2, steps=5000, lr=1e-3, warmup=200,
           weight_decay=0.1, clip=1.0, eval_every=250, ckpt_every=250, eval_windows=200,
           bad_start=3000, bad_len=10, window=50, k=6.0, skip_ahead=20, seed=0)
if SMALL:
    CFG.update(d=32, n_layer=2, n_head=2, ctx=32, batch=8, dropout=0.0, steps=120, lr=3e-3, warmup=10,
               eval_every=20, ckpt_every=20, eval_windows=40, bad_start=80, bad_len=3, window=20)
BAD = set(range(CFG["bad_start"], CFG["bad_start"] + CFG["bad_len"]))
drive = pathlib.Path("/content/drive/MyDrive")
CKPT_DIR = pathlib.Path(os.environ.get("FORGE_CKPT_DIR") or (drive / "forge-L15" if drive.is_dir() and not SMALL else tempfile.mkdtemp(prefix="forge-L15-")))
CKPT_DIR.mkdir(parents=True, exist_ok=True)
print("checkpoints in", CKPT_DIR)

# %% [markdown]
# ## 2. Data at fixed positions
#
# Batch number `pos` is drawn from a generator seeded with `(seed, pos)`, so any batch can be
# regenerated, and skipping data is just moving `pos`. Validation windows are fixed once.

# %%
CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
CORPUS_SHA256 = "86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed"
local = [p for p in (pathlib.Path("data/tinyshakespeare.txt"), pathlib.Path("../data/tinyshakespeare.txt")) if p.exists()]
raw = local[0].read_bytes() if local else urllib.request.urlopen(CORPUS_URL, timeout=60).read()
assert hashlib.sha256(raw).hexdigest() == CORPUS_SHA256, "unexpected corpus contents"
text = raw.decode("utf-8")
chars = sorted(set(text))
VOCAB = len(chars)
stoi = {c: i for i, c in enumerate(chars)}
data = torch.tensor([stoi[c] for c in text], dtype=torch.long)
split = int(0.9 * len(data))
train_data, val_data = data[:split], data[split:]


def get_batch(pos, cfg=CFG, source=None):
    source = train_data if source is None else source
    g = torch.Generator().manual_seed(cfg["seed"] * 1_000_003 + pos)
    ix = torch.randint(len(source) - cfg["ctx"] - 1, (cfg["batch"],), generator=g)
    x = torch.stack([source[i:i + cfg["ctx"]] for i in ix])
    y = torch.stack([source[i + 1:i + cfg["ctx"] + 1] for i in ix])
    if pos in BAD and source is train_data:
        x = torch.randint(VOCAB, x.shape, generator=g)
        y = torch.randint(VOCAB, y.shape, generator=g)
    return x.to(DEVICE), y.to(DEVICE)


_vg = torch.Generator().manual_seed(12345)
VAL_STARTS = torch.randint(len(val_data) - CFG["ctx"] - 1, (CFG["eval_windows"],), generator=_vg)

# %% [markdown]
# ## 3. The model
#
# The L10 GPT with dropout, tied embeddings and PyTorch's fused attention.

# %%
class Block(nn.Module):
    def __init__(self, d, n_head, dropout):
        super().__init__()
        self.n_head, self.dropout = n_head, dropout
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv, self.proj = nn.Linear(d, 3 * d), nn.Linear(d, d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d), nn.Dropout(dropout))
        self.drop = nn.Dropout(dropout)

    def forward(self, x):
        B, T, d = x.shape
        q, k, v = self.qkv(self.ln1(x)).split(d, dim=2)
        q, k, v = (t.view(B, T, self.n_head, d // self.n_head).transpose(1, 2) for t in (q, k, v))
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True, dropout_p=self.dropout if self.training else 0.0)
        x = x + self.drop(self.proj(y.transpose(1, 2).reshape(B, T, d)))
        return x + self.mlp(self.ln2(x))


class GPT(nn.Module):
    def __init__(self, cfg):
        super().__init__()
        self.tok, self.pos = nn.Embedding(VOCAB, cfg["d"]), nn.Embedding(cfg["ctx"], cfg["d"])
        nn.init.normal_(self.tok.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)
        self.drop = nn.Dropout(cfg["dropout"])
        self.blocks = nn.ModuleList([Block(cfg["d"], cfg["n_head"], cfg["dropout"]) for _ in range(cfg["n_layer"])])
        self.ln_f = nn.LayerNorm(cfg["d"])

    def forward(self, idx):
        x = self.drop(self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device)))
        for b in self.blocks:
            x = b(x)
        return self.ln_f(x) @ self.tok.weight.T


# %% [markdown]
# ## 4. The schedule
#
# Write `lr_at(step, cfg)`: linear warmup to `cfg["lr"]` over `cfg["warmup"]` steps, then cosine
# decay to 10% of the peak at `cfg["steps"]`, as a pure function of the step (L15 exercise 5).

# %%
def lr_at(step, cfg=CFG):
    # BEGIN SOLUTION
    if step <= cfg["warmup"]:
        return cfg["lr"] * step / cfg["warmup"]
    progress = min(1.0, (step - cfg["warmup"]) / max(1, cfg["steps"] - cfg["warmup"]))
    return cfg["lr"] * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * progress)))
    # END SOLUTION


# %% [markdown]
# ## 5. Checkpoints
#
# Write `save_checkpoint(path, run)` and `load_checkpoint(path, run)`. `run` is a dictionary with
# the model, optimizer, gradient scaler, `step`, `pos` (the next data position), `skips` and the
# metrics `log`. A checkpoint must hold everything needed to continue exactly: the state dicts, the
# counters, the log, the configuration and the random-number state of the CPU (and of the GPU, if
# there is one), because dropout draws from it. Write to a temporary file and rename it into place,
# so a crash during saving never leaves a half-written checkpoint.

# %%
def save_checkpoint(path, run):
    # BEGIN SOLUTION
    state = {
        "model": run["model"].state_dict(),
        "opt": run["opt"].state_dict(),
        "scaler": run["scaler"].state_dict(),
        "step": run["step"],
        "pos": run["pos"],
        "skips": list(run["skips"]),
        "log": run["log"],
        "cfg": run["cfg"],
        "rng_cpu": torch.get_rng_state(),
        "rng_cuda": torch.cuda.get_rng_state_all() if torch.cuda.is_available() else None,
    }
    tmp = pathlib.Path(str(path) + ".tmp")
    torch.save(state, tmp)
    os.replace(tmp, path)
    # END SOLUTION


def load_checkpoint(path, run):
    # BEGIN SOLUTION
    state = torch.load(path, map_location=DEVICE, weights_only=False)
    run["model"].load_state_dict(state["model"])
    run["opt"].load_state_dict(state["opt"])
    run["scaler"].load_state_dict(state["scaler"])
    run["step"], run["pos"] = state["step"], state["pos"]
    run["skips"], run["log"] = list(state["skips"]), state["log"]
    torch.set_rng_state(state["rng_cpu"])
    if state["rng_cuda"] is not None and torch.cuda.is_available():
        torch.cuda.set_rng_state_all(state["rng_cuda"])
    return run
    # END SOLUTION


def new_run(cfg=CFG):
    torch.manual_seed(cfg["seed"])
    model = GPT(cfg).to(DEVICE)
    opt = torch.optim.AdamW(model.parameters(), lr=cfg["lr"], betas=(0.9, 0.95), weight_decay=cfg["weight_decay"])
    scaler = torch.amp.GradScaler("cuda", enabled=DEVICE == "cuda")
    return {"model": model, "opt": opt, "scaler": scaler, "step": 0, "pos": 0, "skips": [], "log": [], "cfg": cfg}


def train_step(run):
    """One optimizer step on the batch at run["pos"]; returns the loss and the gradient norm before
    clipping. The step count and the data position both advance."""
    cfg, model, opt, scaler = run["cfg"], run["model"], run["opt"], run["scaler"]
    x, y = get_batch(run["pos"], cfg)
    run["step"] += 1
    run["pos"] += 1
    for group in opt.param_groups:
        group["lr"] = lr_at(run["step"], cfg)
    with torch.autocast(device_type="cuda", dtype=torch.float16, enabled=DEVICE == "cuda"):
        loss = F.cross_entropy(model(x).flatten(0, 1).float(), y.flatten())
    opt.zero_grad(set_to_none=True)
    scaler.scale(loss).backward()
    scaler.unscale_(opt)
    norm = torch.nn.utils.clip_grad_norm_(model.parameters(), cfg["clip"]).item()
    scaler.step(opt)
    scaler.update()
    return loss.item(), norm


# %% [markdown]
# ### Exact resume, checked on a tiny model
#
# Ten steps, a checkpoint, ten more steps must give bitwise the same weights as twenty steps
# straight. This check runs on the CPU, where every operation is deterministic.

# %%
def exact_resume_check():
    global DEVICE
    device, DEVICE = DEVICE, "cpu"
    tiny = dict(CFG, d=32, n_layer=2, n_head=2, ctx=16, batch=4, dropout=0.1, steps=20, warmup=5)
    try:
        a = new_run(tiny)
        for _ in range(20):
            train_step(a)
        b = new_run(tiny)
        for _ in range(10):
            train_step(b)
        path = CKPT_DIR / "resume-check.pt"
        save_checkpoint(path, b)
        for _ in range(3):
            train_step(b)  # work after the checkpoint, lost in the "crash"
        c = load_checkpoint(path, new_run(tiny))
        for _ in range(10):
            train_step(c)
        return all(torch.equal(p, q) for p, q in zip(a["model"].parameters(), c["model"].parameters())) and c["step"] == 20
    finally:
        DEVICE = device


resume_exact = exact_resume_check()
print("exact resume:", resume_exact)

# %% [markdown]
# ## 6. Evaluation with error bars
#
# Write `evaluate(model)`: the mean cross-entropy over the fixed validation windows `VAL_STARTS`,
# in evaluation mode and without gradients, with a 95% percentile bootstrap interval over windows
# (2,000 resamples, generator seeded with 0). Return `(mean, low, high, per_window_losses)`.

# %%
@torch.no_grad()
def evaluate(model, cfg=CFG):
    # BEGIN SOLUTION
    model.eval()
    losses = []
    for i in range(0, len(VAL_STARTS), 64):
        idx = VAL_STARTS[i:i + 64]
        x = torch.stack([val_data[j:j + cfg["ctx"]] for j in idx]).to(DEVICE)
        y = torch.stack([val_data[j + 1:j + cfg["ctx"] + 1] for j in idx]).to(DEVICE)
        logits = model(x).float()
        losses.append(F.cross_entropy(logits.transpose(1, 2), y, reduction="none").mean(dim=1).cpu())
    model.train()
    per = torch.cat(losses).numpy()
    rng = np.random.default_rng(0)
    means = per[rng.integers(0, len(per), (2000, len(per)))].mean(axis=1)
    lo, hi = np.quantile(means, [0.025, 0.975])
    return float(per.mean()), float(lo), float(hi), per
    # END SOLUTION


# %% [markdown]
# ## 7. The run
#
# The loop checks each step's loss **before** trusting the update: when it exceeds the mean of the
# previous `window` kept losses by `k` standard deviations, it restores the last checkpoint saved
# before the previous step, moves the data position `skip_ahead` batches past the flagged one, and
# continues (L15 exercises 4 and 9). Write the spike check `is_spike(history, loss, cfg)`; the rest
# of the loop is given. It resumes from the latest checkpoint in `CKPT_DIR` if there is one.

# %%
def is_spike(history, loss, cfg=CFG):
    # BEGIN SOLUTION
    if len(history) < cfg["window"]:
        return False
    prev = np.array(history[-cfg["window"]:])
    return (not math.isfinite(loss)) or loss > prev.mean() + cfg["k"] * prev.std()
    # END SOLUTION


def checkpoint_path(step):
    return CKPT_DIR / f"step-{step:06d}.pt"


run = new_run()
existing = sorted(CKPT_DIR.glob("step-*.pt"))
if existing:
    load_checkpoint(existing[-1], run)
    print("resumed from", existing[-1].name)
else:
    save_checkpoint(checkpoint_path(0), run)
history = [e["loss"] for e in run["log"] if "loss" in e]
spikes = [e for e in run["log"] if e.get("event") == "rollback"]
t0, tokens = time.time(), 0
while run["step"] < CFG["steps"]:
    pos = run["pos"]
    loss, norm = train_step(run)
    tokens += CFG["batch"] * CFG["ctx"]
    if is_spike(history, loss):
        back = (run["step"] - 2) // CFG["ckpt_every"] * CFG["ckpt_every"]
        load_checkpoint(checkpoint_path(back), run)
        event = {"event": "rollback", "flagged_pos": pos, "restored_step": back, "skipped": [run["pos"], pos + CFG["skip_ahead"]]}
        run["log"].append(event)
        run["skips"].append((run["pos"], pos + CFG["skip_ahead"]))
        run["pos"] = pos + CFG["skip_ahead"] + 1
        history = [e["loss"] for e in run["log"] if "loss" in e]
        spikes.append(event)
        print(f"spike at data position {pos} (loss {loss:.2f}); rolled back to step {back}, data now at {run['pos']}")
        continue
    history.append(loss)
    run["log"].append({"step": run["step"], "pos": pos, "loss": loss, "grad_norm": norm, "lr": lr_at(run["step"]),
                       "tokens_per_s": tokens / (time.time() - t0)})
    if run["step"] % CFG["eval_every"] == 0 or run["step"] == CFG["steps"]:
        mean, lo, hi, _ = evaluate(run["model"])
        run["log"].append({"step": run["step"], "event": "eval", "val": mean, "val_low": lo, "val_high": hi})
        print(f"step {run['step']:5d}: train {loss:.3f}, val {mean:.3f} [{lo:.3f}, {hi:.3f}], grad norm {norm:.2f}, "
              f"lr {lr_at(run['step']):.2e}, {tokens / (time.time() - t0):,.0f} tokens/s")
    if run["step"] % CFG["ckpt_every"] == 0:
        save_checkpoint(checkpoint_path(run["step"]), run)

evals = [e for e in run["log"] if e.get("event") == "eval"]
final_val, final_low, final_high, final_per = evaluate(run["model"])
before = [e for e in evals if e["step"] < CFG["bad_start"]]
pre_spike_val = before[-1]["val"] if before else float("nan")
with open(CKPT_DIR / "metrics.json", "w") as f:
    json.dump(run["log"], f)
print(f"final validation loss {final_val:.4f} [{final_low:.4f}, {final_high:.4f}]; {len(spikes)} rollback(s)")

# %% [markdown]
# ## 8. Report
#
# In `REPORT`, write at least 80 words: the configuration, the final validation loss with its
# interval, what happened at the spike (when it was detected, where the run rolled back to and
# which data it skipped), and what you would monitor or change in a longer run.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
spike_text = (
    f"The corrupted shard at data positions {CFG['bad_start']} to {CFG['bad_start'] + CFG['bad_len'] - 1} was flagged at "
    f"position {spikes[0]['flagged_pos']}; the run rolled back to the checkpoint at step {spikes[0]['restored_step']} and "
    f"skipped data up to position {spikes[0]['skipped'][1]}" if spikes else "No spike was detected"
)
REPORT = f"""Run report. A {CFG['n_layer']}-layer GPT of width {CFG['d']} trained for {CFG['steps']} steps on Tiny Shakespeare
with batches of {CFG['batch']} windows of {CFG['ctx']} characters, AdamW with a peak learning rate of {CFG['lr']}, warmup
over {CFG['warmup']} steps, cosine decay and gradient clipping at {CFG['clip']}. {spike_text}. The detector compared each loss
with the mean and standard deviation of the previous {CFG['window']} steps before applying the update. The final validation
loss is {final_val:.3f} nats per character, with a 95% bootstrap interval of [{final_low:.3f}, {final_high:.3f}] over
{CFG['eval_windows']} fixed windows; before the spike it was {pre_spike_val:.3f}. In a longer run I would also monitor the
update-to-weight ratio of each layer and the largest attention logit, keep several checkpoints rather than one per
interval, and audit the logged learning rate after every resume."""
# END SOLUTION
print(REPORT)
