# %% [markdown]
# # L21 capstone: RL with a verifiable reward, and what the KL penalty buys
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. A small GPT is first
# fine-tuned with masked supervised examples (as in L20) to add two-digit numbers, from
# demonstrations in which 30% of the answers contain a slip, as careless human data does. It learns
# the algorithm, and also learns to imitate the slips. You then improve it with reinforcement
# learning against an exact verifier: sample several answers per question, reward the correct ones,
# normalize the rewards within each group, and update the policy with a policy-gradient loss and a
# KL penalty that keeps it near the fine-tuned model. Two penalty strengths are compared on held-out
# questions: accuracy against how far each policy moved. The last cell is the autograder; it prints a completion code to paste into the lesson.

# %%
import copy
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
# ## 1. Configuration
#
# The task is `ab+cd=` followed by the sum and a newline, for two-digit numbers. 500 of the 8,100
# questions are held out before any training. In the supervised data, a fraction `slip` of the
# answers are off by 1 or 10.

# %%
CFG = dict(slip=0.3, d=128, n_layer=4, n_head=4, ctx=16, sft_steps=600, sft_batch=64, sft_lr=1e-3,
           rl_steps=200, prompts=32, group=8, rl_lr=3e-4, betas=[0.01, 1.0], n_test=500, eval_samples=4, seed=0)
if SMALL:
    CFG.update(d=32, n_layer=1, n_head=2, sft_steps=30, rl_steps=4, prompts=4, group=4, n_test=40)

pairs = [(a, b) for a in range(10, 100) for b in range(10, 100)]
np.random.default_rng(CFG["seed"]).shuffle(pairs)
test_pairs, train_pairs = pairs[:CFG["n_test"]], pairs[CFG["n_test"]:]


ANSWER_LEN = 4  # up to three digits and a newline


def prompt_of(a, b):
    return f"{a}+{b}="


def solve(a, b):
    return a + b


# %% [markdown]
# ## 2. The model and its supervised start
#
# A byte-level GPT with a context of 16. Supervised fine-tuning trains on the answer bytes only,
# slips included: maximum likelihood imitates the data, errors and all.
# `sample` draws continuations (greedy or sampled) for a batch of prompts of equal length.

# %%
class Block(nn.Module):
    def __init__(self, d, n_head):
        super().__init__()
        self.d, self.n_head = d, n_head
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv, self.proj = nn.Linear(d, 3 * d), nn.Linear(d, d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def forward(self, x):
        B, T, d = x.shape
        q, k, v = (t.view(B, T, self.n_head, d // self.n_head).transpose(1, 2) for t in self.qkv(self.ln1(x)).split(d, dim=2))
        x = x + self.proj(F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, d))
        return x + self.mlp(self.ln2(x))


class GPT(nn.Module):
    def __init__(self):
        super().__init__()
        d = CFG["d"]
        self.tok, self.pos = nn.Embedding(128, d), nn.Embedding(CFG["ctx"], d)
        nn.init.normal_(self.tok.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)
        self.blocks = nn.ModuleList([Block(d, CFG["n_head"]) for _ in range(CFG["n_layer"])])
        self.ln_f = nn.LayerNorm(d)

    def forward(self, idx):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device))
        for b in self.blocks:
            x = b(x)
        return self.ln_f(x) @ self.tok.weight.T


def sft_batch(n, gen):
    xs, ys, ms = [], [], []
    for _ in range(n):
        a, b = train_pairs[int(gen.integers(len(train_pairs)))]
        answer = solve(a, b)
        if gen.random() < CFG["slip"]:
            answer += int(gen.choice([-10, -1, 1, 10]))
        p, r = prompt_of(a, b).encode(), f"{answer}\n".encode()
        ids, mask = list(p) + list(r), [0] * len(p) + [1] * len(r)
        pad = CFG["ctx"] + 1 - len(ids)
        ids, mask = ids + [10] * pad, mask + [0] * pad
        xs.append(ids[:-1])
        ys.append(ids[1:])
        ms.append(mask[1:])
    return (torch.tensor(xs, device=DEVICE), torch.tensor(ys, device=DEVICE),
            torch.tensor(ms, dtype=torch.float, device=DEVICE))


@torch.no_grad()
def sample(model, prompts, n_new=ANSWER_LEN, greedy=False, gen=None):
    out = torch.tensor([list(p.encode()) for p in prompts], device=DEVICE)
    for _ in range(n_new):
        logits = model(out)[:, -1]
        if greedy:
            nxt = logits.argmax(-1, keepdim=True)
        else:
            nxt = torch.multinomial(F.softmax(logits, -1), 1, generator=gen)
        out = torch.cat([out, nxt], dim=1)
    return out


def answer_text(seq, plen):
    return bytes(seq[plen:].tolist()).decode("ascii", errors="replace").split("\n")[0]


@torch.no_grad()
def correctness(model, pairs_, n=1, greedy=True, seed=4):
    """For each pair, the fraction of n answers (greedy, or sampled at temperature 1) that are right."""
    model.eval()
    g = torch.Generator(device=DEVICE).manual_seed(seed)
    seqs = sample(model, [prompt_of(a, b) for a, b in pairs_ for _ in range(n)], greedy=greedy, gen=g)
    model.train()
    right = [answer_text(s, 6) == str(solve(a, b)) for s, (a, b) in zip(seqs.cpu(), [p for p in pairs_ for _ in range(n)])]
    return np.array(right, dtype=float).reshape(len(pairs_), n).mean(axis=1)


def evaluate(model):
    return dict(greedy=correctness(model, test_pairs),
                sampled=correctness(model, test_pairs, n=CFG["eval_samples"], greedy=False))


torch.manual_seed(CFG["seed"])
sft_model = GPT().to(DEVICE)
opt = torch.optim.AdamW(sft_model.parameters(), lr=CFG["sft_lr"], weight_decay=0.0)
gen = np.random.default_rng(1)
t0 = time.time()
for step in range(1, CFG["sft_steps"] + 1):
    x, y, m = sft_batch(CFG["sft_batch"], gen)
    per = F.cross_entropy(sft_model(x).flatten(0, 1), y.flatten(), reduction="none")
    loss = (per * m.flatten()).sum() / m.sum()
    opt.zero_grad(set_to_none=True)
    loss.backward()
    opt.step()
sft_eval = evaluate(sft_model)
print(f"supervised model after {CFG['sft_steps']} steps ({time.time() - t0:.0f} s): held-out accuracy "
      f"{sft_eval['greedy'].mean():.3f} greedy, {sft_eval['sampled'].mean():.3f} sampled")

# %% [markdown]
# ## 3. Reward and advantages
#
# Write `reward(text, a, b)`: 1.0 if the generated answer (the text before the first newline) is
# exactly the sum, else 0.0. Write `group_advantages(r)` for rewards of shape (prompts, group):
# each reward minus its group's mean, divided by the group's standard deviation plus 1e-6. A group
# whose answers all get the same reward carries no signal.

# %%
def reward(text, a, b):
    # BEGIN SOLUTION
    return float(text == str(solve(a, b)))
    # END SOLUTION


def group_advantages(r):
    # BEGIN SOLUTION
    return (r - r.mean(dim=1, keepdim=True)) / (r.std(dim=1, keepdim=True) + 1e-6)
    # END SOLUTION


# %% [markdown]
# ## 4. The loss
#
# `logp` and `logp_ref` hold, for each sampled response and each generated position, the
# log-probability of the sampled byte under the policy and under the frozen reference (the
# supervised model); `mask` is 1 on the bytes up to and including the first newline. Write
# `rl_loss(logp, logp_ref, adv, mask, beta)`:
#
# $$\mathcal{L} = \frac{1}{\sum m}\sum_{i,t} m_{it}\Bigl(-A_i \log \pi(y_{it}) + \beta\,\bigl(e^{u_{it}} - 1 - u_{it}\bigr)\Bigr),
# \qquad u = \log \pi_\text{ref} - \log \pi.$$
#
# The penalty term is an estimator of the KL divergence whose gradient, unlike that of $-u$, does
# not vanish in expectation (L21 exercise on KL estimators).

# %%
def rl_loss(logp, logp_ref, adv, mask, beta):
    # BEGIN SOLUTION
    u = logp_ref - logp
    per = -adv[:, None] * logp + beta * (torch.exp(u) - 1 - u)
    return (per * mask).sum() / mask.sum()
    # END SOLUTION


def response_logprobs(model, seqs, plen):
    logits = model(seqs[:, :-1])
    return F.log_softmax(logits, -1).gather(-1, seqs[:, 1:, None])[..., 0][:, plen - 1:]


def response_mask(seqs, plen):
    gen_tok = seqs[:, plen:]
    seen = torch.cumsum((gen_tok == 10).long(), dim=1)
    return ((seen == 0) | ((seen == 1) & (gen_tok == 10))).float()


@torch.no_grad()
def kl_to_ref(policy, ref, pairs_, n=4, seed=5):
    """KL(policy || reference) per response: along responses sampled from the policy, the exact KL
    between the two next-byte distributions at each generated position, summed over the response."""
    g = torch.Generator(device=DEVICE).manual_seed(seed)
    seqs = sample(policy, [prompt_of(a, b) for a, b in pairs_ for _ in range(n)], gen=g)
    m = response_mask(seqs, 6)
    lp = F.log_softmax(policy(seqs[:, :-1]), -1)[:, 5:]
    lr = F.log_softmax(ref(seqs[:, :-1]), -1)[:, 5:]
    return float(((lp.exp() * (lp - lr)).sum(-1) * m).sum(1).mean())


# %% [markdown]
# ## 5. Train with two penalty strengths
#
# Each run starts from the supervised model and sees the same prompts. Every step samples
# `group` answers for each of `prompts` questions, scores them, and takes one gradient step.

# %%
def run_rl(beta):
    torch.manual_seed(CFG["seed"])
    policy = copy.deepcopy(sft_model)
    opt = torch.optim.AdamW(policy.parameters(), lr=CFG["rl_lr"], weight_decay=0.0)
    g = torch.Generator(device=DEVICE).manual_seed(2)
    rng = np.random.default_rng(3)
    log = []
    for step in range(CFG["rl_steps"]):
        batch = [train_pairs[int(i)] for i in rng.integers(len(train_pairs), size=CFG["prompts"])]
        flat = [p for p in batch for _ in range(CFG["group"])]
        seqs = sample(policy, [prompt_of(a, b) for a, b in flat], gen=g)
        r = torch.tensor([reward(answer_text(s, 6), a, b) for s, (a, b) in zip(seqs.cpu(), flat)], device=DEVICE)
        adv = group_advantages(r.view(CFG["prompts"], CFG["group"])).flatten()
        mask = response_mask(seqs, 6)
        logp = response_logprobs(policy, seqs, 6)
        with torch.no_grad():
            logp_ref = response_logprobs(sft_model, seqs, 6)
        loss = rl_loss(logp, logp_ref, adv, mask, beta)
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
        opt.step()
        log.append(float(r.mean()))
    return policy, log


runs = {}
for beta in CFG["betas"]:
    t0 = time.time()
    policy, log = run_rl(beta)
    ev = evaluate(policy)
    runs[beta] = dict(eval=ev, train_reward=log, kl=kl_to_ref(policy, sft_model, test_pairs[:100]))
    print(f"beta {beta}: held-out accuracy {ev['greedy'].mean():.3f} greedy, {ev['sampled'].mean():.3f} sampled; training "
          f"reward {np.mean(log[:10]):.2f} -> {np.mean(log[-10:]):.2f}; KL to the supervised model {runs[beta]['kl']:.3f} "
          f"nats per answer ({time.time() - t0:.0f} s)")

# %% [markdown]
# ## 6. Did RL help?
#
# Compare each policy with the supervised model on the same held-out questions, item by item, with
# a paired bootstrap interval on the accuracy gain (L23 makes this the default). Sampled accuracy is
# what the model does when it is used with sampling, and what the reward trained; greedy accuracy is
# its single most likely answer.

# %%
def paired_gain(after, before, n_boot=2000, seed=0):
    d = after - before
    means = d[np.random.default_rng(seed).integers(0, len(d), (n_boot, len(d)))].mean(axis=1)
    return float(d.mean()), *np.quantile(means, [0.025, 0.975]).tolist()


gains = {beta: paired_gain(runs[beta]["eval"]["sampled"], sft_eval["sampled"]) for beta in CFG["betas"]}
greedy_gains = {beta: paired_gain(runs[beta]["eval"]["greedy"], sft_eval["greedy"]) for beta in CFG["betas"]}
for beta in CFG["betas"]:
    (g, lo, hi), (gg, glo, ghi) = gains[beta], greedy_gains[beta]
    print(f"beta {beta}: sampled accuracy gain {g:+.3f} [{lo:+.3f}, {hi:+.3f}], greedy {gg:+.3f} [{glo:+.3f}, {ghi:+.3f}], "
          f"KL {runs[beta]['kl']:.3f}")
low_beta, high_beta = min(CFG["betas"]), max(CFG["betas"])

# %% [markdown]
# ## 7. Report
#
# In `REPORT`, write at least 80 words: the supervised accuracy, each policy's accuracy gain with
# its interval and its KL from the supervised model, the tradeoff between them, and why an exact
# reward on held-out questions is harder to hack than a learned reward model.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
lo_g, hi_g = gains[low_beta], gains[high_beta]
REPORT = f"""RL report. Trained on demonstrations with {CFG['slip']:.0%} slips, the supervised model answered {sft_eval['greedy'].mean():.1%} of
{len(test_pairs)} held-out sums correctly when decoding greedily but only {sft_eval['sampled'].mean():.1%} when sampling: it learned the
algorithm and also the habit of slipping. RL with an exact-match reward, group-relative advantages over {CFG['group']} samples
per question and {CFG['rl_steps']} steps raised sampled accuracy by {lo_g[0]:+.3f} [{lo_g[1]:+.3f}, {lo_g[2]:+.3f}] with a KL penalty of
{low_beta}, moving the policy {runs[low_beta]['kl']:.3f} nats per answer from the supervised model, and by {hi_g[0]:+.3f}
[{hi_g[1]:+.3f}, {hi_g[2]:+.3f}] with a penalty of {high_beta}, at a KL of {runs[high_beta]['kl']:.3f}. That is the reward-KL tradeoff:
the strong penalty holds the policy near a reference that slips, so it can remove only part of the slips. Here the
reference is worse than the verifier and a weak penalty is right; with a learned reward model, whose errors the policy
would exploit as it moved away, the penalty is what keeps the reward trustworthy. The intervals are paired over the same
questions, and the exact-match reward is the task itself, evaluated on questions never seen in training."""
# END SOLUTION
print(REPORT)
