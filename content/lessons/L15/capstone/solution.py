# %% [markdown]
# # L15 capstone: predict a training run before you train it
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. You will train a
# sweep of small character-level GPTs (the L14 model) over five widths and four token counts on
# Tiny Shakespeare, fit the scaling law $L(N, D) = E + A N^{-\alpha} + B D^{-\beta}$ to the runs,
# derive the compute-optimal frontier from it, and predict the validation loss of a larger model
# **before** training it. The last cell is the autograder; it prints a completion code to paste
# into the lesson.

# %%
import hashlib
import math
import os
import pathlib
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
# ## 1. The corpus
#
# The same Tiny Shakespeare file as in L13, read character by character. The validation split is
# the last 10% of the text; every run is scored on all of it.

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
split = int(0.9 * len(data))
train_data, val_data = data[:split], data[split:]
print(f"{len(train_data):,} training and {len(val_data):,} validation characters")

# %% [markdown]
# ## 2. The model and its size
#
# L14's GPT with the output layer tied to the character embedding. Scaling laws count
# **non-embedding** parameters: write `non_embedding_params(model)`, the number of parameters
# outside the token and position embeddings.

# %%
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


def non_embedding_params(model):
    # BEGIN SOLUTION
    return sum(p.numel() for name, p in model.named_parameters() if not name.startswith(("tok.", "pos.")))
    # END SOLUTION


# %% [markdown]
# ## 3. One training run
#
# Every model has four layers and heads of width 16; only the width $d$ changes, so the sweep
# varies one thing. Every run takes the same number of optimizer steps, and the token budget sets
# the batch size: small models early in training learn more per token from small batches, and real
# runs grow the batch with the budget. AdamW uses a learning rate of $0.4/d$ (the best rate shrinks
# with width, L15 exercise 12), a linear warmup over the first 10% of steps and a cosine decay to
# 10% of the peak **at the end of that run's own budget**: a run cut short of its schedule
# understates what its token count can achieve. `val_loss` scores the whole validation split.

# %%
CFG = dict(ctx=128, steps=1950, n_layer=4, widths=[32, 48, 64, 96, 128], batches=[2, 4, 8, 16], heldout_width=192)
if SMALL:
    CFG.update(ctx=32, steps=100, n_layer=2, widths=[16, 24, 32], batches=[4, 8, 16], heldout_width=48)
CTX, STEPS, N_LAYER = CFG["ctx"], CFG["steps"], CFG["n_layer"]


@torch.no_grad()
def val_loss(model):
    model.eval()
    n = (len(val_data) - 1) // CTX
    x = val_data[: n * CTX].view(n, CTX)
    y = val_data[1: n * CTX + 1].view(n, CTX)
    total = 0.0
    for i in range(0, n, 256):
        logits = model(x[i:i + 256].to(DEVICE))
        total += F.cross_entropy(logits.flatten(0, 1), y[i:i + 256].to(DEVICE).flatten(), reduction="sum").item()
    model.train()
    return total / (n * CTX)


def train_run(d, batch, seed=0):
    torch.manual_seed(seed)
    model = GPT(len(chars), CTX, d, N_LAYER, d // 16).to(DEVICE)
    lr = 0.4 / d
    opt = torch.optim.AdamW(model.parameters(), lr=lr, betas=(0.9, 0.95), weight_decay=0.1)
    steps = STEPS
    warmup = max(1, steps // 10)
    gen = torch.Generator().manual_seed(seed)
    for step in range(1, steps + 1):
        for group in opt.param_groups:
            group["lr"] = lr * min(1.0, step / warmup) * (0.1 + 0.45 * (1 + math.cos(math.pi * step / steps)))
        ix = torch.randint(len(train_data) - CTX - 1, (batch,), generator=gen)
        x = torch.stack([train_data[i:i + CTX] for i in ix]).to(DEVICE)
        y = torch.stack([train_data[i + 1:i + CTX + 1] for i in ix]).to(DEVICE)
        loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
    N = non_embedding_params(model)
    D = steps * batch * CTX
    return {"d": d, "batch": batch, "N": N, "D": D, "C": 6 * N * D, "loss": val_loss(model)}


# %% [markdown]
# ## 4. The sweep
#
# Twenty runs: every width at every token budget. The largest budget is about four epochs of the
# training text, the limit beyond which repeated data loses value quickly (L15 exercise 10).

# %%
runs = []
t0 = time.time()
for d in CFG["widths"]:
    for batch in CFG["batches"]:
        runs.append(train_run(d, batch))
        r = runs[-1]
        print(f"d = {d:3d}: N = {r['N']:>8,}  D = {r['D']:>9,}  C = {r['C']:.2e}  loss {r['loss']:.4f}  ({time.time() - t0:.0f} s)")
N = np.array([r["N"] for r in runs], dtype=float)
D = np.array([r["D"] for r in runs], dtype=float)
L = np.array([r["loss"] for r in runs])

# %% [markdown]
# ## 5. Fit the scaling law
#
# Fit $L = E + A N^{-\alpha} + B D^{-\beta}$ to the twenty runs the way you did in exercise 5:
# for fixed exponents, $(E, A, B)$ follow from least squares on the relative errors; search
# $\alpha, \beta$ over 0.02, 0.04, ..., 1.50, then over a grid ten times finer within 0.02 of the
# best pair. One change: a loss floor below zero means nothing, so `fit_for_exponents` refits with
# $E = 0$ whenever the free solve gives $E < 0$. Return a dictionary with keys `E, A, B, alpha, beta`.

# %%
def law(N, D, E, A, B, alpha, beta):
    return E + A * N ** -alpha + B * D ** -beta


def fit_for_exponents(alpha, beta, N, D, L):
    X = np.stack([np.ones_like(N), N ** -alpha, D ** -beta], axis=1) / L[:, None]
    coef = np.linalg.lstsq(X, np.ones_like(L), rcond=None)[0]
    if coef[0] < 0:
        coef = np.r_[0.0, np.linalg.lstsq(X[:, 1:], np.ones_like(L), rcond=None)[0]]
    r = X @ coef - 1
    return coef[0], coef[1], coef[2], float(r @ r)


def fit_parametric(N, D, L):
    # BEGIN SOLUTION
    def search(alphas, betas, best):
        for a in alphas:
            for b in betas:
                fit = fit_for_exponents(a, b, N, D, L)
                if best is None or fit[3] < best[0]:
                    best = (fit[3], a, b, fit)
        return best

    coarse = np.arange(0.02, 1.501, 0.02)
    best = search(coarse, coarse, None)
    fine = np.arange(-0.02, 0.0201, 0.002)
    best = search(best[1] + fine, best[2] + fine, best)
    _, a, b, (E, A, B, _) = best
    return {"E": E, "A": A, "B": B, "alpha": a, "beta": b}
    # END SOLUTION


fit = fit_parametric(N, D, L)
pred = law(N, D, **fit)
fit_rmse = float(np.sqrt(np.mean((pred / L - 1) ** 2)))
print("fit:", {k: round(float(v), 4) for k, v in fit.items()}, f"relative RMS error {fit_rmse:.2%}")

# %% [markdown]
# ## 6. The compute-optimal frontier, with and without enough data
#
# From the fit, the best split of a budget $C = 6ND$ is
# $N^* = G (C/6)^{\beta/(\alpha+\beta)}$ with $G = (\alpha A / \beta B)^{1/(\alpha+\beta)}$ (L15,
# section 3). Write `optimal_allocation(C, fit)` returning $(N^*, D^*, L^*)$. But the corpus is
# finite: at most `D_MAX` tokens (four epochs). Write `constrained_allocation(C, fit, d_max)`, which
# uses the unconstrained optimum when $D^* \le$ `d_max` and otherwise spends the budget on
# parameters, $D = $ `d_max`, $N = C / (6\,$`d_max`$)$, since the loss falls in both $N$ and $D$.

# %%
D_MAX = max(r["D"] for r in runs)


def optimal_allocation(C, fit):
    # BEGIN SOLUTION
    a, b = fit["alpha"], fit["beta"]
    G = (a * fit["A"] / (b * fit["B"])) ** (1 / (a + b))
    n = G * (C / 6) ** (b / (a + b))
    d_ = C / (6 * n)
    return n, d_, law(n, d_, **fit)
    # END SOLUTION


def constrained_allocation(C, fit, d_max):
    # BEGIN SOLUTION
    n, d_, l = optimal_allocation(C, fit)
    if d_ <= d_max:
        return n, d_, l
    n = C / (6 * d_max)
    return n, d_max, law(n, d_max, **fit)
    # END SOLUTION


budgets = np.logspace(np.log10(min(r["C"] for r in runs)), np.log10(max(r["C"] for r in runs)), 5)
exponent_N = fit["beta"] / (fit["alpha"] + fit["beta"])
print(f"unconstrained: N* grows as C^{exponent_N:.2f}")
for c in budgets:
    n, d_, l = optimal_allocation(c, fit)
    nc, dc, lc = constrained_allocation(c, fit, D_MAX)
    best_run = min((r for r in runs if r["C"] <= c * 1.05), key=lambda r: r["loss"], default=None)
    seen = f"; best run trained at or below it: d = {best_run['d']}, D = {best_run['D']:,}, loss {best_run['loss']:.3f}" if best_run else ""
    print(f"C = {c:.2e}: unconstrained N* = {n:,.0f} on D* = {d_:,.0f}; with D <= {D_MAX:,}: N = {nc:,.0f}, L = {lc:.3f}{seen}")

# %% [markdown]
# ## 7. Predict, then train
#
# The held-out model is larger than any in the sweep. Write down the fit's prediction for it at the
# largest token budget **before** training it; the cell records the time of the prediction. Then
# train it and compare.

# %%
HD = CFG["heldout_width"]
probe = GPT(len(chars), CTX, HD, N_LAYER, HD // 16)
heldout_N, heldout_D = non_embedding_params(probe), max(r["D"] for r in runs)
prediction = float(law(heldout_N, heldout_D, **fit))
predicted_at = time.time()
print(f"prediction for N = {heldout_N:,}, D = {heldout_D:,}: {prediction:.4f} nats per character")

# %%
heldout_started = time.time()
heldout = train_run(HD, max(CFG["batches"]))
prediction_error = (prediction - heldout["loss"]) / heldout["loss"]
print(f"held-out run: {heldout['loss']:.4f}; predicted {prediction:.4f} ({prediction_error:+.2%})")

# %% [markdown]
# ## 8. Report
#
# In `REPORT`, write at least 80 words: the fitted exponents and what they say about splitting a
# budget, how close the prediction was, and one reason a fit on this sweep could mislead at much
# larger scale.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
big = optimal_allocation(budgets[-1], fit)
frontier_text = (
    f"Its unconstrained optimum at the largest budget is a {big[0]:,.0f}-parameter model on {big[1]:,.0f} tokens, far more than\n"
    "the corpus holds, so with the corpus capped at four epochs the data limit binds and extra compute can only go into\n"
    "parameters."
    if big[1] > D_MAX
    else f"On the frontier N* grows as C^{exponent_N:.2f}, and within this sweep the corpus holds enough tokens for the optimum."
)
REPORT = f"""The fit gives alpha = {fit['alpha']:.2f} for parameters and beta = {fit['beta']:.2f} for tokens, with an
irreducible loss E = {fit['E']:.2f} nats per character and a relative RMS error of {fit_rmse:.1%} over {len(runs)} runs.
{frontier_text}
I predicted {prediction:.3f} for the held-out model before training it and measured {heldout['loss']:.3f},
an error of {prediction_error:+.1%}. The fit could mislead at much larger scale: these runs are early in training,
where the loss still falls roughly linearly in the logarithm of the tokens, so the floor is not determined
({'the fit puts it at zero' if fit['E'] < 1e-9 else 'the fitted value is a weak constraint'}) and the exponents describe this regime only. The sweep also covers at most four epochs
of one small corpus, and the learning-rate rule was not tuned per size. A bootstrap over the runs would show how
wide the uncertainty of the exponents is."""
# END SOLUTION
print(REPORT)
