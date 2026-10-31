# %% [markdown]
# # L23 capstone: find a circuit and prove it
#
# Choose **Runtime, Change runtime type, T4 GPU** (the notebook also runs on a CPU runtime in a few
# minutes), then run the cells in order. A two-layer, attention-only transformer learns to continue
# sequences in which a random block of tokens repeats. You locate the heads that do it from their
# attention patterns, test them with ablations against ablating every other head, measure with
# activation patching how much of the behaviour each head carries, and check a prediction the
# mechanism makes about inputs the model never trained on. The last cell is the autograder; it
# prints a completion code to paste into the lesson.

# %%
import math
import os
import time

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

SMALL = os.environ.get("SMALL") == "1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", torch.cuda.get_device_name(0) if DEVICE == "cuda" else "CPU")

# %% [markdown]
# ## 1. The task and the model
#
# Each training sequence holds `ctx` random tokens from a vocabulary of `vocab`, except that a
# block of 12 to 30 of them appears twice, at random places. Tokens in the first copy are
# unpredictable; from the second token of the second copy on, each one can be found by looking up
# the previous token's earlier occurrence and copying what followed it.
#
# The model has token embeddings, two attention layers with no MLPs, and an unembedding. Positions
# enter only as a learned bias on each head's attention score for each distance between query and
# key, as in T5 and ALiBi. (With absolute position embeddings this task has a second solution: a
# layer-0 head attends to the earlier copy of the current token and copies its position, and a
# layer-1 head attends to the position after it. Models trained that way often find it instead of
# the circuit below; relative positions leave only the classic one.) Each layer computes the output
# of every head separately before adding them to the residual stream, and accepts a
# `hook(layer, outputs)` that may replace them: that is how we ablate and patch heads.

# %%
CFG = dict(vocab=64, ctx=64, d=64, n_head=4, n_layer=2, block=(12, 30), steps=3000, batch=64, lr=3e-3, seed=0,
           eval_n=512)
if SMALL:
    CFG.update(steps=200, eval_n=64)
V, T, H = CFG["vocab"], CFG["ctx"], CFG["n_head"]


def make_batch(n, gen):
    """Sequences with one repeated block; info holds (s1, s2, L): the two starts and the length."""
    x = torch.randint(0, V, (n, T), generator=gen)
    info = []
    for b in range(n):
        L = int(torch.randint(CFG["block"][0], CFG["block"][1] + 1, (1,), generator=gen))
        s1 = int(torch.randint(0, T - 2 * L + 1, (1,), generator=gen))
        s2 = int(torch.randint(s1 + L, T - L + 1, (1,), generator=gen))
        x[b, s2:s2 + L] = x[b, s1:s1 + L]
        info.append((s1, s2, L))
    return x, info


def repeat_mask(info):
    """mask[b, t] is True where the token at position t + 1 is predictable: inside the second copy,
    after its first token. It indexes the predictions made at position t."""
    mask = torch.zeros(len(info), T - 1, dtype=torch.bool)
    for b, (s1, s2, L) in enumerate(info):
        mask[b, s2:s2 + L - 1] = True
    return mask


class Attention(nn.Module):
    def __init__(self, d, n_head):
        super().__init__()
        self.n_head, self.dh = n_head, d // n_head
        self.qkv = nn.Linear(d, 3 * d, bias=False)
        self.out = nn.Linear(d, d, bias=False)
        self.rel = nn.Parameter(torch.zeros(n_head, T))  # a bias for each head and distance

    def forward(self, x):
        B, T_, d = x.shape
        q, k, v = (t.view(B, T_, self.n_head, self.dh).transpose(1, 2) for t in self.qkv(x).split(d, dim=2))
        dist = (torch.arange(T_, device=x.device)[:, None] - torch.arange(T_, device=x.device)[None, :]).clamp(min=0)
        scores = (q @ k.transpose(-1, -2)) / math.sqrt(self.dh) + self.rel[:, dist]
        causal = torch.ones(T_, T_, dtype=torch.bool, device=x.device).triu(1)
        att = scores.masked_fill(causal, float("-inf")).softmax(dim=-1)
        z = att @ v
        W = self.out.weight.view(d, self.n_head, self.dh)
        return torch.einsum("bhtk,ehk->bhte", z, W), att


class AttnOnly(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok = nn.Embedding(V, CFG["d"])
        self.layers = nn.ModuleList([Attention(CFG["d"], H) for _ in range(CFG["n_layer"])])
        self.unembed = nn.Linear(CFG["d"], V, bias=False)

    def forward(self, x, hook=None):
        """Return the logits, the attention patterns (one (B, H, T, T) tensor per layer) and the
        per-head outputs (one (B, H, T, d) tensor per layer, after any hook)."""
        r = self.tok(x)
        atts, outs = [], []
        for layer, attn in enumerate(self.layers):
            o, a = attn(r)
            if hook is not None:
                o = hook(layer, o)
            atts.append(a)
            outs.append(o)
            r = r + o.sum(dim=1)
        return self.unembed(r), atts, outs


def token_logprobs(logits, x):
    """log p(x[:, t + 1]) at every position t, shape (B, T - 1)."""
    return torch.log_softmax(logits[:, :-1], dim=-1).gather(-1, x[:, 1:, None])[..., 0]


torch.manual_seed(CFG["seed"])
model = AttnOnly().to(DEVICE)
opt = torch.optim.AdamW(model.parameters(), lr=CFG["lr"], weight_decay=0.01)
gen = torch.Generator().manual_seed(1)
t0 = time.time()
for step in range(1, CFG["steps"] + 1):
    x, info = make_batch(CFG["batch"], gen)
    x = x.to(DEVICE)
    logits, _, _ = model(x)
    loss = F.cross_entropy(logits[:, :-1].reshape(-1, V), x[:, 1:].reshape(-1))
    opt.zero_grad(set_to_none=True)
    loss.backward()
    opt.step()
    if step % 500 == 0 or step == CFG["steps"]:
        with torch.no_grad():
            rep = -token_logprobs(logits, x)[repeat_mask(info).to(DEVICE)].mean().item()
        print(f"step {step}: loss {loss.item():.3f}, loss on repeated tokens {rep:.3f} ({time.time() - t0:.0f} s)")
model.eval()

# A fixed evaluation batch, used by every measurement below.
x_eval, info_eval = make_batch(CFG["eval_n"], torch.Generator().manual_seed(7))
x_eval, mask_eval = x_eval.to(DEVICE), repeat_mask(info_eval).to(DEVICE)
first_mask = torch.zeros_like(mask_eval)
for b, (s1, s2, L) in enumerate(info_eval):
    first_mask[b, s1:s1 + L - 1] = True
with torch.no_grad():
    logits, atts, outs = model(x_eval)
    lp = token_logprobs(logits, x_eval)
loss_first, loss_repeat = -lp[first_mask].mean().item(), -lp[mask_eval].mean().item()
print(f"loss on the first copy {loss_first:.3f} (uniform guessing: ln {V} = {math.log(V):.3f}); "
      f"on the second copy {loss_repeat:.3f}")

# %% [markdown]
# ## 2. Read the attention patterns
#
# Write `head_scores(atts, info)`, returning two arrays of shape (layers, heads):
#
# - the **previous-token score**: the average attention from each position $t \ge 1$ to $t - 1$;
# - the **induction score**: over the positions $t$ of the second copy whose next token is
#   predictable (from $s_2$ to $s_2 + L - 2$), the average attention to the position just after the
#   earlier occurrence of the current token, $s_1 + (t - s_2) + 1$.
#
# Then pick the heads: `prev_heads` are the layer-0 heads with a previous-token score above 0.3,
# and `induction_heads` the layer-1 heads with an induction score above 0.3, each a list of
# (layer, head) pairs.

# %%
def head_scores(atts, info):
    # BEGIN SOLUTION
    n_layer, n_head = len(atts), atts[0].shape[1]
    prev = np.zeros((n_layer, n_head))
    induction = np.zeros((n_layer, n_head))
    t = torch.arange(1, atts[0].shape[-1])
    rows, cols, bs = [], [], []
    for b, (s1, s2, L) in enumerate(info):
        for q in range(s2, s2 + L - 1):
            bs.append(b)
            rows.append(q)
            cols.append(s1 + (q - s2) + 1)
    bs, rows, cols = (torch.tensor(v) for v in (bs, rows, cols))
    for layer, a in enumerate(atts):
        a = a.detach().cpu()
        prev[layer] = a[:, :, t, t - 1].mean(dim=(0, 2)).numpy()
        induction[layer] = a[bs, :, rows, cols].mean(dim=0).numpy()
    return prev, induction
    # END SOLUTION


prev_score, induction_score = head_scores(atts, info_eval)
print("previous-token scores\n", prev_score.round(2))
print("induction scores\n", induction_score.round(2))
# BEGIN SOLUTION -> prev_heads = ;; induction_heads =
prev_heads = [(0, h) for h in range(H) if prev_score[0, h] > 0.3]
induction_heads = [(1, h) for h in range(H) if induction_score[1, h] > 0.3]
# END SOLUTION
print("previous-token heads:", prev_heads, " induction heads:", induction_heads)

# %% [markdown]
# ## 3. Necessity: ablate the heads
#
# Write `ablated_loss(heads)`: the loss on the second copy (`mask_eval`) when the outputs of the
# given heads are replaced by their **mean** output, averaged over the evaluation batch at each
# position (`mean_outs[layer][h]`, shape (T, d)). Mean ablation removes what a head says about this
# particular input while keeping its typical contribution, so the rest of the network sees
# activations of the usual size.
#
# The circuit should be necessary: ablating its previous-token heads, or its induction heads,
# should each send the loss on the second copy back toward uniform guessing. The baseline is
# ablating every head outside the circuit. The table of single-head ablations shows how the work
# is shared out, including any redundancy among heads.

# %%
mean_outs = [o.mean(dim=0) for o in outs]


@torch.no_grad()
def ablated_loss(heads):
    # BEGIN SOLUTION
    def hook(layer, o):
        o = o.clone()
        for l, h in heads:
            if l == layer:
                o[:, h] = mean_outs[layer][h]
        return o

    logits, _, _ = model(x_eval, hook=hook)
    return -token_logprobs(logits, x_eval)[mask_eval].mean().item()
    # END SOLUTION


circuit = prev_heads + induction_heads
complement = [(layer, h) for layer in range(2) for h in range(H) if (layer, h) not in circuit]
single = np.array([[ablated_loss([(layer, h)]) for h in range(H)] for layer in range(2)])
loss_prev_ablated = ablated_loss(prev_heads)
loss_induction_ablated = ablated_loss(induction_heads)
loss_circuit_ablated = ablated_loss(circuit)
loss_complement_ablated = ablated_loss(complement)
print("loss on the second copy with one head ablated\n", single.round(2))
print(f"loss on the second copy: intact {loss_repeat:.3f}; ablated: previous-token heads {loss_prev_ablated:.3f}, "
      f"induction heads {loss_induction_ablated:.3f}, whole circuit {loss_circuit_ablated:.3f}, "
      f"every other head {loss_complement_ablated:.3f}")

# %% [markdown]
# ## 4. Sufficiency: patch the heads
#
# The **corrupted** input is the evaluation batch with the first copy of each block replaced by
# fresh random tokens, so nothing earlier predicts the second copy. The metric is the mean
# log-probability of the clean next tokens on the second copy. Write
# `patch_effect(heads)`: run the corrupted input with the given heads' outputs replaced by their
# outputs on the clean input, and return the restored fraction
# $(m_\text{patched} - m_\text{corrupt}) / (m_\text{clean} - m_\text{corrupt})$.
#
# Before running it, predict what patching only the previous-token heads will restore. (They
# make the induction heads attend to the right place; but in the corrupted run, what sits at that
# place?)

# %%
x_corrupt = x_eval.clone()
gen_c = torch.Generator().manual_seed(11)
for b, (s1, s2, L) in enumerate(info_eval):
    x_corrupt[b, s1:s1 + L] = torch.randint(0, V, (L,), generator=gen_c).to(DEVICE)


@torch.no_grad()
def metric(logits):
    return token_logprobs(logits, x_eval)[mask_eval].mean().item()


with torch.no_grad():
    clean_logits, _, clean_outs = model(x_eval)
    corrupt_logits, _, _ = model(x_corrupt)
m_clean, m_corrupt = metric(clean_logits), metric(corrupt_logits)


@torch.no_grad()
def patch_effect(heads):
    # BEGIN SOLUTION
    def hook(layer, o):
        o = o.clone()
        for l, h in heads:
            if l == layer:
                o[:, h] = clean_outs[layer][:, h]
        return o

    logits, _, _ = model(x_corrupt, hook=hook)
    return (metric(logits) - m_corrupt) / (m_clean - m_corrupt)
    # END SOLUTION


effects = np.array([[patch_effect([(layer, h)]) for h in range(H)] for layer in range(2)])
circuit_effect = patch_effect(circuit)
prev_effect = patch_effect(prev_heads)
print(f"metric: clean {m_clean:.3f}, corrupted {m_corrupt:.3f}")
print("restored fraction, one head at a time\n", effects.round(2))
print(f"patching the whole circuit restores {circuit_effect:.2f}; the previous-token heads alone {prev_effect:.2f}")

# %% [markdown]
# ## 5. A prediction on new inputs
#
# The mechanism predicts more than the training task: any token that appeared earlier should
# raise the probability of whatever followed it then, even for a single pair rather than a block.
# Each test sequence is random except for a pair $[A][B]$ at a random place and a later $[A]$; the
# model's top prediction after the second $[A]$ should be $[B]$. The control sequences are the same
# with the earlier $[A]$ replaced, so the only route to $[B]$ is removed. Write
# `pair_accuracy(x, pos)`: the fraction of sequences whose top prediction at position `pos[i]` is the
# token `x[i, pos[i] + 1]`, with a bootstrap interval over sequences (exercise 1).

# %%
def make_pairs(n, gen, control=False):
    x = torch.randint(0, V, (n, T), generator=gen)
    pos = torch.zeros(n, dtype=torch.long)
    for i in range(n):
        a_pos = int(torch.randint(0, T // 2, (1,), generator=gen))
        q = int(torch.randint(a_pos + 2, T - 1, (1,), generator=gen))
        a, b = int(x[i, a_pos]), int(torch.randint(0, V, (1,), generator=gen))
        x[i, a_pos + 1] = b
        x[i, q] = a
        x[i, q + 1] = b
        if control:
            x[i, a_pos] = (a + 1 + int(torch.randint(0, V - 1, (1,), generator=gen))) % V
        pos[i] = q
    return x.to(DEVICE), pos.to(DEVICE)


@torch.no_grad()
def pair_accuracy(x, pos, n_boot=2000, seed=0):
    # BEGIN SOLUTION
    logits, _, _ = model(x)
    rows = torch.arange(len(pos), device=x.device)
    correct = (logits[rows, pos].argmax(dim=-1) == x[rows, pos + 1]).float().cpu().numpy()
    rng = np.random.default_rng(seed)
    means = correct[rng.integers(0, len(correct), (n_boot, len(correct)))].mean(axis=1)
    lo, hi = np.quantile(means, [0.025, 0.975])
    return float(correct.mean()), float(lo), float(hi)
    # END SOLUTION


pairs_acc = pair_accuracy(*make_pairs(CFG["eval_n"], torch.Generator().manual_seed(21)))
control_acc = pair_accuracy(*make_pairs(CFG["eval_n"], torch.Generator().manual_seed(21), control=True))
print(f"top-1 accuracy predicting [B]: {pairs_acc[0]:.2f} [{pairs_acc[1]:.2f}, {pairs_acc[2]:.2f}] with the earlier pair, "
      f"{control_acc[0]:.2f} [{control_acc[1]:.2f}, {control_acc[2]:.2f}] without it (chance {1 / V:.3f})")

# %% [markdown]
# ## 6. Report
#
# In `REPORT`, write at least 80 words: the circuit you found (which heads, and what each one's
# attention pattern shows), the evidence for necessity and sufficiency against the baseline, the
# prediction and its result, and one thing the account leaves unexplained.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
others_hurt = [(l, h) for l, h in complement if single[l, h] > loss_repeat + 0.3]
odd_text = (
    f"Single-head ablations show that {others_hurt} also matter although their attention scores do not mark them, a "
    f"role this account does not explain" if others_hurt else
    "No head outside the circuit matters much on its own"
)
REPORT = f"""Circuit report. A two-layer attention-only model reduced its loss on the second copy of a repeated block
to {loss_repeat:.2f} nats, against {loss_first:.2f} on the unpredictable first copy. Attention scores single out
previous-token head(s) {prev_heads} in layer 0 (scores {', '.join(f'{prev_score[l, h]:.2f}' for l, h in prev_heads)}), which attend to the
position before each token, and induction head(s) {induction_heads} in layer 1 (scores
{', '.join(f'{induction_score[l, h]:.2f}' for l, h in induction_heads)}), which attend to the position just after the earlier occurrence of the
current token and copy it. Necessity: mean-ablating the previous-token heads raises the loss on the second copy to
{loss_prev_ablated:.2f} and ablating the induction heads to {loss_induction_ablated:.2f} (uniform guessing is {math.log(V):.2f}), while ablating every
other head gives {loss_complement_ablated:.2f}. Sufficiency: patching the circuit's clean outputs into the corrupted run restores
{circuit_effect:.2f} of the metric; the previous-token heads alone restore {prev_effect:.2f}, because they only steer the
induction heads to a position whose token was corrupted. The induction heads share the work: ablating any one of them
raises the loss to at most {max([single[l, h] for l, h in induction_heads], default=loss_repeat):.2f}. The mechanism predicts copying after a single earlier pair, never
trained on: top-1 accuracy is {pairs_acc[0]:.2f} [{pairs_acc[1]:.2f}, {pairs_acc[2]:.2f}] with the pair and {control_acc[0]:.2f} without it.
{odd_text}; and patching whole head outputs does not separate composition through keys from composition through
queries or values, which path patching would test."""
# END SOLUTION
print(REPORT)
