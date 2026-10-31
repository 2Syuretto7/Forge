# %% [markdown]
# # L20 capstone: from a raw crawl to a served model
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order; the whole pipeline
# takes roughly 10 to 20 minutes. It runs the six stages your design document planned: clean a noisy crawl
# (L12), pretrain a byte-level GPT on it (L15), fine-tune it with LoRA on two tasks (L16), improve
# one task with RL against an exact verifier (L17), evaluate every stage with intervals over items
# (L19), and serve the final model with a key-value cache and continuous batching (L18). The tools
# from those lessons are provided, solved; you write the decisions and the glue: the plan, the
# cleaning order, the reward, the evaluation of each stage, the manifest, and the final report.
# Mount Google Drive first (`from google.colab import drive; drive.mount('/content/drive')`) and the
# pretraining checkpoint survives a disconnected session. The last cell is the autograder; it prints
# a completion code to paste into the lesson.

# %%
import copy
import hashlib
import json
import math
import os
import pathlib
import re
import tempfile
import time
import urllib.request
import zlib

import numpy as np
import torch
import torch.nn as nn
import torch.nn.functional as F

SMALL = os.environ.get("SMALL") == "1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
print("device:", torch.cuda.get_device_name(0) if DEVICE == "cuda" else "CPU")
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False
drive = pathlib.Path("/content/drive/MyDrive")
CKPT_DIR = drive / "forge-L20" if drive.exists() else pathlib.Path(tempfile.mkdtemp(prefix="forge-L20-"))
CKPT_DIR.mkdir(parents=True, exist_ok=True)
print("checkpoints in", CKPT_DIR)

# %% [markdown]
# ## 1. The plan
#
# Write `PLAN` from your design document: the pretraining model and run, the fine-tuning and RL
# settings. The pretraining compute, $6ND$, must fit in `BUDGET` floating-point operations (about
# 20 minutes of a T4 at the utilization small models reach). The cell prints what the plan implies.

# %%
BUDGET = 3e15
# BEGIN SOLUTION -> PLAN = dict(pretrain=dict(), sft=dict(), rl=dict())
PLAN = dict(
    pretrain=dict(d=384, n_layer=6, n_head=6, ctx=256, batch=32, steps=3000, lr=1e-3, warmup=200, dropout=0.2,
                  eval_every=250),
    sft=dict(rank=16, alpha=32, lr=2e-3, steps=1500, batch=32, replay=2.0),
    rl=dict(task="REVERSE", steps=150, prompts=16, group=8, lr=3e-5, beta=0.02),
)
# END SOLUTION
if SMALL:
    PLAN["pretrain"].update(d=64, n_layer=2, n_head=2, ctx=64, batch=8, steps=60, warmup=10, eval_every=30)
    PLAN["sft"].update(steps=30)
    PLAN["rl"].update(steps=3, prompts=4, group=4)
P = PLAN["pretrain"]


def n_params(d, n_layer, ctx, vocab=256):
    return n_layer * 12 * d * d + (vocab + ctx) * d


plan_params = n_params(P["d"], P["n_layer"], P["ctx"])
plan_tokens = P["steps"] * P["batch"] * P["ctx"]
plan_flops = 6 * plan_params * plan_tokens
print(f"pretraining: {plan_params / 1e6:.1f} million parameters, {plan_tokens / 1e6:.1f} million tokens, "
      f"{plan_flops:.2e} FLOPs ({plan_flops / BUDGET:.0%} of the budget)")

# %% [markdown]
# ## 2. The crawl and the evaluation sets
#
# Tiny Shakespeare is split once: 80% is the source of the crawl, 10% is validation text (some of
# which leaks into the crawl), 10% is test text. The task words for fine-tuning are split into
# training and test words here, before any training, and never change.

# %%
CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
CORPUS_SHA256 = "86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed"
local = [p for p in (pathlib.Path("data/tinyshakespeare.txt"), pathlib.Path("../data/tinyshakespeare.txt")) if p.exists()]
raw_bytes = local[0].read_bytes() if local else urllib.request.urlopen(CORPUS_URL, timeout=60).read()
assert hashlib.sha256(raw_bytes).hexdigest() == CORPUS_SHA256, "unexpected corpus contents"
text = raw_bytes.decode("utf-8")
n = len(text)
source_text, val_text, test_text = text[: int(0.8 * n)], text[int(0.8 * n): int(0.9 * n)], text[int(0.9 * n):]


def chunk_docs(t, size=1000):
    docs, cur = [], ""
    for block in t.split("\n\n"):
        cur += block + "\n\n"
        if len(cur) >= size:
            docs.append(cur.strip())
            cur = ""
    if cur.strip():
        docs.append(cur.strip())
    return docs


source_docs, val_docs = chunk_docs(source_text), chunk_docs(val_text)
FOOTER = "Share this page: Facebook | Twitter | Email | Print"
SPAM = "buy cheap free best deal online discount offer click now win prize casino bonus".split()


def make_crawl(seed=0):
    """The noisy crawl of L12: exact and near copies, footers, junk, and leaked validation text."""
    rng = np.random.default_rng(seed)

    def perturb(doc, rate):
        w = doc.split(" ")
        for i in range(len(w)):
            if rng.random() < rate:
                w[i] = w[rng.integers(len(w))]
        return " ".join(w)

    crawl = [(d + ("\n" + FOOTER if rng.random() < 0.6 else ""), "source") for d in source_docs]
    for i in rng.choice(len(source_docs), len(source_docs) // 10, replace=False):
        crawl += [(source_docs[i].upper() if rng.random() < 0.3 else source_docs[i].replace("\n", "\n "), "exact")
                  for _ in range(10)]
    for i in rng.choice(len(source_docs), len(source_docs) // 10, replace=False):
        crawl += [(perturb(source_docs[i], 0.03), "near") for _ in range(3)]
    for _ in range(len(source_docs) // 4):
        kind = rng.integers(3)
        if kind == 0:
            junk = " ".join(rng.choice(SPAM, 200))
        elif kind == 1:
            junk = "\n".join(" | ".join(str(v) for v in rng.integers(0, 10000, 6)) for _ in range(40))
        else:
            junk = bytes(rng.integers(33, 127, 1000).tolist()).decode("ascii")
        crawl.append((junk, "junk"))
    for i in rng.choice(len(val_docs), len(val_docs) // 10, replace=False):
        crawl += [(val_docs[i], "leak") for _ in range(40)]
    order = rng.permutation(len(crawl))
    return [crawl[i][0] for i in order], [crawl[i][1] for i in order]


raw_docs, kinds = make_crawl()
TASKS = {"UPPER": lambda w: w.upper(), "REVERSE": lambda w: w[::-1]}
words = sorted({w for w in re.findall(r"[a-z]+", text.lower()) if 3 <= len(w) <= 8})
np.random.default_rng(0).shuffle(words)
n_test_words = 300 if not SMALL else 24
test_words, train_words = words[:n_test_words], words[n_test_words:]
print(f"{len(raw_docs)} crawl documents; {len(train_words)} training words, {len(test_words)} test words")

# %% [markdown]
# ## 3. Stage 1: clean the crawl
#
# The functions of L12 are provided. Write `clean_crawl(docs)`: run them in the right order and
# return the indices of the documents kept. Decontaminate against the validation documents.

# %%
def normalize(doc):
    return " ".join(doc.lower().split())


def exact_dedup(docs):
    seen, keep = set(), []
    for i, d in enumerate(docs):
        h = hashlib.sha1(normalize(d).encode("utf-8")).hexdigest()
        if h not in seen:
            seen.add(h)
            keep.append(i)
    return keep


def strip_boilerplate(docs, min_docs):
    counts = {}
    for d in docs:
        for line in {l.strip() for l in d.split("\n") if l.strip()}:
            counts[line] = counts.get(line, 0) + 1
    common = {line for line, c in counts.items() if c >= min_docs}
    return ["\n".join(l for l in d.split("\n") if l.strip() not in common) for d in docs]


STOP_WORDS = {"the", "be", "to", "of", "and", "that", "have", "with"}


def passes_quality(doc):
    words_ = doc.split()
    if not 50 <= len(words_) <= 100_000:
        return False
    mean_len = sum(map(len, words_)) / len(words_)
    alpha = sum(any(c.isalpha() for c in w) for w in words_) / len(words_)
    stops = {w.strip(".,;:!?\"'()").lower() for w in words_} & STOP_WORDS
    symbols = max(doc.count("#"), doc.count("...")) / len(words_)
    return 3 <= mean_len <= 10 and alpha >= 0.8 and len(stops) >= 2 and symbols <= 0.1


PRIME = 2 ** 31 - 1
_hrng = np.random.default_rng(1)
HASH_A, HASH_B = _hrng.integers(1, PRIME, 128), _hrng.integers(0, PRIME, 128)


def minhash(doc):
    t = normalize(doc)
    sh = {t[i:i + 5] for i in range(len(t) - 4)} or {t}
    x = np.array(sorted(zlib.crc32(s.encode("utf-8")) for s in sh), dtype=np.int64) % PRIME
    return ((np.outer(HASH_A, x) + HASH_B[:, None]) % PRIME).min(axis=1)


def near_dedup(signatures, bands=16, rows=8, min_similarity=0.7):
    parent = list(range(len(signatures)))

    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i

    buckets = {}
    for i, sig in enumerate(signatures):
        for band in range(bands):
            buckets.setdefault((band, tuple(sig[band * rows:(band + 1) * rows].tolist())), []).append(i)
    for members in buckets.values():
        for j in members[1:]:
            if np.mean(signatures[j] == signatures[members[0]]) >= min_similarity:
                ri, rj = find(j), find(members[0])
                parent[max(ri, rj)] = min(ri, rj)
    return sorted({find(i) for i in range(len(signatures))})


def words_of(doc):
    return [w for w in (x.strip(".,;:!?\"'()[]").lower() for x in doc.split()) if w]


def decontaminate(docs, eval_docs, n=13):
    index = set()
    for d in eval_docs:
        w = words_of(d)
        index |= {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}
    return [j for j, d in enumerate(docs)
            if not any(tuple(words_of(d)[i:i + n]) in index for i in range(len(words_of(d)) - n + 1))]


def clean_crawl(docs):
    """Indices of the crawl documents kept, and the cleaned texts (footer lines removed)."""
    # BEGIN SOLUTION
    cleaned = strip_boilerplate(docs, min_docs=50)
    kept = [i for i in exact_dedup(cleaned) if passes_quality(cleaned[i])]
    kept = [kept[j] for j in near_dedup([minhash(cleaned[i]) for i in kept])]
    kept = [kept[j] for j in decontaminate([cleaned[i] for i in kept], val_docs)]
    return kept, cleaned
    # END SOLUTION


t0 = time.time()
kept, cleaned = clean_crawl(raw_docs)
kept_kinds = [kinds[i] for i in kept]
corpus = "\n\n".join(cleaned[i] for i in kept)
print(f"cleaned in {time.time() - t0:.0f} s: kept {len(kept)} of {len(raw_docs)} documents, "
      f"{len(corpus):,} characters; " + ", ".join(f"{k} {kept_kinds.count(k)}/{kinds.count(k)}" for k in sorted(set(kinds))))

# %% [markdown]
# ## 4. The manifest
#
# Every stage records a digest of what it read, of its configuration, and of what it wrote
# (L20 exercise 10). Write `record(stage, input_digest, config, output_digest)`, which appends a
# record to `MANIFEST` and returns the output digest, and `check_chain(records, first_input)`.

# %%
MANIFEST = []


def digest(obj):
    if isinstance(obj, nn.Module):
        h = hashlib.sha256()
        for k, v in sorted(obj.state_dict().items()):
            h.update(k.encode())
            h.update(v.detach().float().cpu().numpy().tobytes())
        return h.hexdigest()[:12]
    return hashlib.sha256(json.dumps(obj, sort_keys=True).encode("utf-8")).hexdigest()[:12]


def record(stage, input_digest, config, output_digest):
    # BEGIN SOLUTION
    MANIFEST.append({"stage": stage, "input": input_digest, "config": digest(config), "output": output_digest})
    return output_digest
    # END SOLUTION


def check_chain(records, first_input):
    # BEGIN SOLUTION
    expected = first_input
    for i, r in enumerate(records):
        if r["input"] != expected:
            return i
        expected = r["output"]
    return None
    # END SOLUTION


raw_digest = digest(raw_docs)
corpus_digest = record("clean", raw_digest, dict(min_docs=50, bands=16, rows=8, min_similarity=0.7, n=13), digest(corpus))

# %% [markdown]
# ## 5. Stage 2: pretrain
#
# The GPT of L18 with dropout, trained on the cleaned corpus with warmup and cosine decay, gradient
# clipping and, on a GPU, 16-bit mixed precision with loss scaling (L13). It evaluates on the
# validation text every `eval_every` steps, keeps the best weights, and checkpoints so a restarted
# session continues where it stopped (L15).

# %%
class Block(nn.Module):
    def __init__(self, d, n_head, dropout=0.0):
        super().__init__()
        self.d, self.n_head = d, n_head
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv, self.proj = nn.Linear(d, 3 * d), nn.Linear(d, d)
        self.fc1, self.fc2 = nn.Linear(d, 4 * d), nn.Linear(4 * d, d)
        self.drop = nn.Dropout(dropout)

    def heads(self, t):
        B, T, _ = t.shape
        return t.view(B, T, self.n_head, self.d // self.n_head).transpose(1, 2)

    def merge(self, t):
        B, _, T, _ = t.shape
        return t.transpose(1, 2).reshape(B, T, self.d)

    def mlp(self, x):
        return self.fc2(F.gelu(self.fc1(self.ln2(x))))

    def forward(self, x):
        q, k, v = (self.heads(t) for t in self.qkv(self.ln1(x)).split(self.d, dim=2))
        x = x + self.drop(self.proj(self.merge(F.scaled_dot_product_attention(q, k, v, is_causal=True))))
        return x + self.drop(self.mlp(x))


class GPT(nn.Module):
    def __init__(self, d, n_layer, n_head, ctx, dropout=0.0):
        super().__init__()
        self.d, self.n_head, self.ctx = d, n_head, ctx
        self.tok, self.pos = nn.Embedding(256, d), nn.Embedding(ctx, d)
        nn.init.normal_(self.tok.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)
        self.blocks = nn.ModuleList([Block(d, n_head, dropout) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)

    def head(self, x):
        return self.ln_f(x) @ self.tok.weight.T

    def forward(self, idx):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device))
        for b in self.blocks:
            x = b(x)
        return self.head(x)


train_ids = torch.tensor(list(corpus.encode("utf-8")), dtype=torch.long)
val_ids = torch.tensor(list(val_text.encode("utf-8")), dtype=torch.long)
CTX = P["ctx"]
_vg = torch.Generator().manual_seed(1)
VAL_STARTS = torch.randint(len(val_ids) - CTX - 1, (64 if not SMALL else 8,), generator=_vg)


@torch.no_grad()
def val_loss(model):
    was = model.training
    model.eval()
    x = torch.stack([val_ids[i:i + CTX] for i in VAL_STARTS]).to(DEVICE)
    y = torch.stack([val_ids[i + 1:i + CTX + 1] for i in VAL_STARTS]).to(DEVICE)
    loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten()).item()
    model.train(was)
    return loss


def lr_at(step):
    if step <= P["warmup"]:
        return P["lr"] * step / P["warmup"]
    progress = (step - P["warmup"]) / (P["steps"] - P["warmup"])
    return P["lr"] * (0.1 + 0.9 * 0.5 * (1 + math.cos(math.pi * progress)))


def pretrain():
    torch.manual_seed(0)
    model = GPT(P["d"], P["n_layer"], P["n_head"], CTX, P["dropout"]).to(DEVICE)
    opt = torch.optim.AdamW(model.parameters(), lr=P["lr"], betas=(0.9, 0.95), weight_decay=0.1)
    scaler = torch.amp.GradScaler("cuda", enabled=DEVICE == "cuda")
    state = dict(step=0, best=float("inf"), log=[])
    path = CKPT_DIR / f"pretrain-{digest(P)}-{corpus_digest}.pt"
    if path.exists():
        ck = torch.load(path, map_location=DEVICE, weights_only=False)
        model.load_state_dict(ck["model"])
        opt.load_state_dict(ck["opt"])
        scaler.load_state_dict(ck["scaler"])
        state = ck["state"]
        print(f"resumed at step {state['step']}")
    t0 = time.time()
    while state["step"] < P["steps"]:
        step = state["step"] + 1
        g = torch.Generator().manual_seed(1000 + step)  # the batch depends only on the step
        ix = torch.randint(len(train_ids) - CTX - 1, (P["batch"],), generator=g)
        x = torch.stack([train_ids[i:i + CTX] for i in ix]).to(DEVICE)
        y = torch.stack([train_ids[i + 1:i + CTX + 1] for i in ix]).to(DEVICE)
        for group in opt.param_groups:
            group["lr"] = lr_at(step)
        with torch.autocast("cuda", dtype=torch.float16, enabled=DEVICE == "cuda"):
            loss = F.cross_entropy(model(x).flatten(0, 1).float(), y.flatten())
        opt.zero_grad(set_to_none=True)
        scaler.scale(loss).backward()
        scaler.unscale_(opt)
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        scaler.step(opt)
        scaler.update()
        state["step"] = step
        if step % P["eval_every"] == 0 or step == P["steps"]:
            v = val_loss(model)
            state["log"].append(dict(step=step, train=loss.item(), val=v))
            if v < state["best"]:
                state["best"] = v
                torch.save(model.state_dict(), CKPT_DIR / "pretrain-best.pt")
            torch.save(dict(model=model.state_dict(), opt=opt.state_dict(), scaler=scaler.state_dict(), state=state),
                       path.with_suffix(".tmp"))
            os.replace(path.with_suffix(".tmp"), path)
            print(f"step {step}: train {loss.item():.3f}, validation {v:.3f} ({time.time() - t0:.0f} s)")
    model.load_state_dict(torch.load(CKPT_DIR / "pretrain-best.pt", map_location=DEVICE))
    model.eval()
    return model, state


base_model, pretrain_state = pretrain()
pretrain_val = val_loss(base_model)
print(f"best validation loss {pretrain_val:.3f} nats per byte")
base_digest = record("pretrain", corpus_digest, P, digest(base_model))

# %% [markdown]
# ## 6. Evaluating a stage
#
# Write `evaluate_stage(model)`, returning a dict with: the validation loss (`"val"`), and for each
# task the per-word correctness of greedy decoding on the test words (`"UPPER"`, `"REVERSE"`, arrays
# of 0/1) and the per-word fraction correct of four sampled answers (`"UPPER_sampled"`,
# `"REVERSE_sampled"`). Use `answers`, which decodes prompts of equal length in one batch, and
# group the words by length. Then `interval` gives a bootstrap interval for any per-item array.

# %%
def prompt_of(task, word):
    return f"{task}: {word}\n="


@torch.no_grad()
def generate_ids(model, task, batch_words, greedy=True, n=1, seed=0):
    """Prompts (all words the same length, n copies each) followed by len(word) + 1 decoded bytes."""
    L = len(batch_words[0])
    ids = torch.tensor([list(prompt_of(task, w).encode()) for w in batch_words for _ in range(n)], device=DEVICE)
    g = torch.Generator(device=DEVICE).manual_seed(seed)
    for _ in range(L + 1):
        logits = model(ids)[:, -1].float()
        nxt = logits.argmax(-1, keepdim=True) if greedy else torch.multinomial(F.softmax(logits, -1), 1, generator=g)
        ids = torch.cat([ids, nxt], dim=1)
    return ids


def to_texts(ids, L):
    return [bytes(row[-(L + 1):].tolist()).decode("utf-8", errors="replace") for row in ids.cpu()]


def answers(model, task, batch_words, greedy=True, n=1, seed=0):
    """The decoded answers, n per word, each len(word) + 1 bytes long."""
    return to_texts(generate_ids(model, task, batch_words, greedy, n, seed), len(batch_words[0]))


def interval(x, n_boot=2000, seed=0):
    x = np.asarray(x, dtype=float)
    means = x[np.random.default_rng(seed).integers(0, len(x), (n_boot, len(x)))].mean(axis=1)
    return float(x.mean()), *np.quantile(means, [0.025, 0.975]).tolist()


def evaluate_stage(model):
    # BEGIN SOLUTION
    model.eval()
    result = {"val": val_loss(model)}
    by_len = {}
    for i, w in enumerate(test_words):
        by_len.setdefault(len(w), []).append(i)
    for task, fn in TASKS.items():
        greedy = np.zeros(len(test_words))
        sampled = np.zeros(len(test_words))
        for L, idx in by_len.items():
            ws = [test_words[i] for i in idx]
            g = answers(model, task, ws)
            s = answers(model, task, ws, greedy=False, n=4, seed=L)
            for j, i in enumerate(idx):
                target = fn(test_words[i]) + "\n"
                greedy[i] = g[j] == target
                sampled[i] = np.mean([a == target for a in s[4 * j:4 * j + 4]])
        result[task], result[task + "_sampled"] = greedy, sampled
    return result
    # END SOLUTION


STAGES = {"pretrained": evaluate_stage(base_model)}


def show_stage(name):
    r = STAGES[name]
    parts = [f"val {r['val']:.3f}"]
    for task in TASKS:
        m, lo, hi = interval(r[task])
        ms, los, his = interval(r[task + "_sampled"])
        parts.append(f"{task} {m:.2f} [{lo:.2f}, {hi:.2f}] greedy, {ms:.2f} [{los:.2f}, {his:.2f}] sampled")
    print(f"{name:>10}: " + "; ".join(parts))


show_stage("pretrained")

# %% [markdown]
# ## 7. Stage 3: fine-tune with LoRA
#
# The LoRA layer and the masked instruction loss of L16, trained on the training words with
# pretraining text replayed at weight `replay` (8 windows per step) to limit forgetting, then merged
# into the weights.

# %%
class LoRALinear(nn.Module):
    def __init__(self, base_layer, r, alpha):
        super().__init__()
        self.base, self.r, self.alpha = base_layer, r, alpha
        dev = base_layer.weight.device
        self.A = nn.Parameter(torch.randn(r, base_layer.in_features, device=dev) / math.sqrt(base_layer.in_features))
        self.B = nn.Parameter(torch.zeros(base_layer.out_features, r, device=dev))

    def forward(self, x):
        return self.base(x) + (self.alpha / self.r) * (x @ self.A.T) @ self.B.T

    def merged(self):
        layer = copy.deepcopy(self.base)
        layer.weight.data += (self.alpha / self.r) * self.B.data @ self.A.data
        return layer


LINEARS = ["qkv", "proj", "fc1", "fc2"]


def sft_batch(n, rng):
    xs, ys, ms = [], [], []
    for _ in range(n):
        task = list(TASKS)[int(rng.integers(2))]
        w = train_words[int(rng.integers(len(train_words)))]
        p, a = prompt_of(task, w).encode(), (TASKS[task](w) + "\n").encode()
        ids, mask = list(p) + list(a), [0] * len(p) + [1] * len(a)
        pad = 32 - len(ids)
        ids, mask = ids + [10] * pad, mask + [0] * pad
        xs.append(ids[:-1])
        ys.append(ids[1:])
        ms.append(mask[1:])
    return (torch.tensor(xs, device=DEVICE), torch.tensor(ys, device=DEVICE),
            torch.tensor(ms, dtype=torch.float, device=DEVICE))


def finetune(base):
    S = PLAN["sft"]
    model = copy.deepcopy(base)
    for p in model.parameters():
        p.requires_grad_(False)
    for b in model.blocks:
        for name in LINEARS:
            setattr(b, name, LoRALinear(getattr(b, name), S["rank"], S["alpha"]))
    params = [p for p in model.parameters() if p.requires_grad]
    opt = torch.optim.AdamW(params, lr=S["lr"], weight_decay=0.0)
    rng = np.random.default_rng(1)
    replay_gen = torch.Generator().manual_seed(2)
    model.train()
    for step in range(1, S["steps"] + 1):
        for group in opt.param_groups:
            group["lr"] = S["lr"] * min(1.0, step / 50)
        x, y, m = sft_batch(S["batch"], rng)
        per = F.cross_entropy(model(x).flatten(0, 1), y.flatten(), reduction="none")
        loss = (per * m.flatten()).sum() / m.sum()
        if S.get("replay"):
            ix = torch.randint(len(train_ids) - CTX - 1, (8,), generator=replay_gen)
            xr = torch.stack([train_ids[i:i + CTX] for i in ix]).to(DEVICE)
            yr = torch.stack([train_ids[i + 1:i + CTX + 1] for i in ix]).to(DEVICE)
            loss = loss + S["replay"] * F.cross_entropy(model(xr).flatten(0, 1), yr.flatten())
        opt.zero_grad(set_to_none=True)
        loss.backward()
        opt.step()
    for b in model.blocks:
        for name in LINEARS:
            setattr(b, name, getattr(b, name).merged())
    for p in model.parameters():
        p.requires_grad_(True)
    model.eval()
    return model, sum(p.numel() for p in params)


t0 = time.time()
sft_model, sft_trainable = finetune(base_model)
STAGES["fine-tuned"] = evaluate_stage(sft_model)
print(f"fine-tuned {sft_trainable:,} adapter parameters in {time.time() - t0:.0f} s")
show_stage("fine-tuned")
sft_digest = record("finetune", base_digest, PLAN["sft"], digest(sft_model))

# %% [markdown]
# ## 8. Stage 4: RL against an exact verifier
#
# Write `rl_reward(task, word, text)`: 1.0 if the generated text is exactly the right answer
# followed by a newline, else 0.0. The loop of L17 then samples a
# group of answers per training word, normalizes rewards within each group, and updates the policy
# with the policy-gradient loss and the KL penalty to the fine-tuned model.

# %%
def rl_reward(task, word, text):
    # BEGIN SOLUTION
    return float(text == TASKS[task](word) + "\n")
    # END SOLUTION


def run_rl(start):
    R = PLAN["rl"]
    task = R["task"]
    policy, ref = copy.deepcopy(start), copy.deepcopy(start)
    policy.eval()  # no dropout: the policy that samples is the policy that is scored
    opt = torch.optim.AdamW(policy.parameters(), lr=R["lr"], weight_decay=0.0)
    rng = np.random.default_rng(3)
    by_len = {}
    for w in train_words:
        by_len.setdefault(len(w), []).append(w)
    lengths = sorted(by_len)
    log = []
    for step in range(R["steps"]):
        L = lengths[int(rng.integers(len(lengths)))]
        batch = [by_len[L][int(i)] for i in rng.integers(len(by_len[L]), size=R["prompts"])]
        seqs = generate_ids(policy, task, batch, greedy=False, n=R["group"], seed=step)
        texts = to_texts(seqs, L)
        r = torch.tensor([rl_reward(task, w, t) for w, t in zip([w for w in batch for _ in range(R["group"])], texts)],
                         device=DEVICE).view(R["prompts"], R["group"])
        adv = ((r - r.mean(1, keepdim=True)) / (r.std(1, keepdim=True) + 1e-6)).flatten()
        plen = seqs.shape[1] - (L + 1)
        logp = F.log_softmax(policy(seqs[:, :-1]), -1).gather(-1, seqs[:, 1:, None])[..., 0][:, plen - 1:]
        with torch.no_grad():
            logp_ref = F.log_softmax(ref(seqs[:, :-1]), -1).gather(-1, seqs[:, 1:, None])[..., 0][:, plen - 1:]
        u = logp_ref - logp
        loss = (-adv[:, None] * logp + R["beta"] * (u.exp() - 1 - u)).mean()
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(policy.parameters(), 1.0)
        opt.step()
        log.append(float(r.mean()))
    policy.eval()
    return policy, log


t0 = time.time()
rl_model, rl_log = run_rl(sft_model)
STAGES["RL"] = evaluate_stage(rl_model)
print(f"RL on {PLAN['rl']['task']}: training reward {np.mean(rl_log[:10]):.2f} -> {np.mean(rl_log[-10:]):.2f} "
      f"({time.time() - t0:.0f} s)")
show_stage("RL")
rl_digest = record("rl", sft_digest, PLAN["rl"], digest(rl_model))


def paired(after, before):
    return interval(np.asarray(after) - np.asarray(before))


rl_task = PLAN["rl"]["task"]
rl_gain = paired(STAGES["RL"][rl_task + "_sampled"], STAGES["fine-tuned"][rl_task + "_sampled"])
print(f"RL changed sampled {rl_task} accuracy by {rl_gain[0]:+.3f} [{rl_gain[1]:+.3f}, {rl_gain[2]:+.3f}] (paired over words)")

# %% [markdown]
# ## 9. Stage 5: serve
#
# The serving engine of L18, solved: prefill and decode over a key-value cache, and the
# continuous-batching loop. The final model serves 64 task requests arriving at 40 per second;
# every served answer is checked against full recomputation.

# %%
class KVCache:
    def __init__(self, model, slots, max_len):
        shape = (len(model.blocks), slots, model.n_head, max_len, model.d // model.n_head)
        self.k = torch.zeros(shape, device=DEVICE)
        self.v = torch.zeros(shape, device=DEVICE)
        self.lengths = torch.zeros(slots, dtype=torch.long, device=DEVICE)


@torch.no_grad()
def prefill(model, cache, slot, prompt):
    ids = torch.tensor([prompt], device=DEVICE)
    T = ids.shape[1]
    x = model.tok(ids) + model.pos(torch.arange(T, device=DEVICE))
    for layer, b in enumerate(model.blocks):
        q, k, v = (b.heads(t) for t in b.qkv(b.ln1(x)).split(b.d, dim=2))
        cache.k[layer, slot, :, :T], cache.v[layer, slot, :, :T] = k[0], v[0]
        x = x + b.proj(b.merge(F.scaled_dot_product_attention(q, k, v, is_causal=True)))
        x = x + b.mlp(x)
    cache.lengths[slot] = T
    return model.head(x[0, -1])


@torch.no_grad()
def decode_step(model, cache, slots, tokens):
    s = torch.as_tensor(slots, device=DEVICE)
    pos = cache.lengths[s]
    width = int(pos.max()) + 1
    mask = (torch.arange(width, device=DEVICE)[None, :] <= pos[:, None])[:, None, None, :]
    x = (model.tok(torch.as_tensor(tokens, device=DEVICE)) + model.pos(pos))[:, None, :]
    for layer, b in enumerate(model.blocks):
        q, k, v = (b.heads(t) for t in b.qkv(b.ln1(x)).split(b.d, dim=2))
        cache.k[layer, s, :, pos], cache.v[layer, s, :, pos] = k[:, :, 0], v[:, :, 0]
        K, V = cache.k[layer, s, :, :width], cache.v[layer, s, :, :width]
        x = x + b.proj(b.merge(F.scaled_dot_product_attention(q, K, V, attn_mask=mask)))
        x = x + b.mlp(x)
    cache.lengths[s] += 1
    return model.head(x[:, 0])


def serve(model, requests, max_batch):
    cache = KVCache(model, max_batch, model.ctx)
    queue = sorted(requests, key=lambda r: r["arrival"])
    free, active, done = list(range(max_batch))[::-1], {}, {}
    start, i = time.perf_counter(), 0
    now = lambda: time.perf_counter() - start
    while i < len(queue) or active:
        while i < len(queue) and free and queue[i]["arrival"] <= now():
            r = queue[i]
            i += 1
            slot = free.pop()
            rec = dict(id=r["id"], arrival=r["arrival"], tokens=[int(prefill(model, cache, slot, r["prompt"]).argmax())],
                       times=[now()])
            if len(rec["tokens"]) == r["max_new"]:
                done[r["id"]] = rec
                free.append(slot)
            else:
                active[slot] = (r, rec)
        if not active:
            if i < len(queue):
                time.sleep(max(0.0, min(queue[i]["arrival"] - now(), 0.002)))
            continue
        slots = list(active)
        nxt = decode_step(model, cache, slots, [active[s][1]["tokens"][-1] for s in slots]).argmax(-1).tolist()
        t = now()
        for s, tok in zip(slots, nxt):
            r, rec = active[s]
            rec["tokens"].append(tok)
            rec["times"].append(t)
            if len(rec["tokens"]) == r["max_new"]:
                done[r["id"]] = rec
                free.append(s)
                del active[s]
    return [done[r["id"]] for r in requests]


@torch.no_grad()
def generate_reference(model, prompt, n):
    ids = torch.tensor([prompt], device=DEVICE)
    out = []
    for _ in range(n):
        nxt = int(model(ids)[0, -1].argmax())
        out.append(nxt)
        ids = torch.cat([ids, torch.tensor([[nxt]], device=DEVICE)], dim=1)
    return out


wl = np.random.default_rng(5)
arrivals = np.cumsum(wl.exponential(1 / 40, 64 if not SMALL else 8))
requests = []
for j, t in enumerate(arrivals - arrivals[0]):
    task, w = list(TASKS)[j % 2], test_words[int(wl.integers(len(test_words)))]
    requests.append(dict(id=j, arrival=float(t), task=task, word=w, prompt=list(prompt_of(task, w).encode()),
                         max_new=len(w) + 1))
final_model = rl_model
serve(final_model, requests[:4], 32)
served = serve(final_model, requests, 32)
served_match = float(np.mean([rec["tokens"] == generate_reference(final_model, r["prompt"], r["max_new"])
                              for rec, r in zip(served, requests)]))
itl = np.concatenate([np.diff(rec["times"]) for rec in served])
ttft = np.array([rec["times"][0] - rec["arrival"] for rec in served])
served_acc = float(np.mean([bytes(rec["tokens"]).decode("utf-8", errors="replace") == TASKS[r["task"]](r["word"]) + "\n"
                            for rec, r in zip(served, requests)]))
serving = dict(p95_itl_ms=1e3 * float(np.percentile(itl, 95)), p95_ttft_ms=1e3 * float(np.percentile(ttft, 95)),
               match=served_match, accuracy=served_acc)
print(f"served {len(requests)} requests: p95 between tokens {serving['p95_itl_ms']:.1f} ms, p95 to first token "
      f"{serving['p95_ttft_ms']:.1f} ms, {served_match:.0%} match recomputation, {served_acc:.0%} answered correctly")
record("serve", rl_digest, dict(slots=32, rate=40, requests=len(requests)), digest([rec["tokens"] for rec in served]))
chain_break = check_chain(MANIFEST, raw_digest)
print(json.dumps(MANIFEST, indent=1))
print("manifest chain intact" if chain_break is None else f"manifest chain broken at stage {chain_break}")

# %% [markdown]
# ## 10. The final report
#
# In `REPORT`, write at least 200 words: every stage's result with its interval, what each stage
# changed and what it cost, the serving numbers, what went wrong or surprised you, and what you
# would do with ten times the compute. Compare it with the predictions in your design document.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
def acc(stage, task, kind=""):
    m, lo, hi = interval(STAGES[stage][task + kind])
    return f"{m:.2f} [{lo:.2f}, {hi:.2f}]"


best_step = min(pretrain_state["log"], key=lambda e: e["val"])["step"]
harder = min(TASKS, key=lambda t: STAGES["fine-tuned"][t].mean())
easier = max(TASKS, key=lambda t: STAGES["fine-tuned"][t].mean())
sample_gap = STAGES["fine-tuned"][rl_task].mean() - STAGES["fine-tuned"][rl_task + "_sampled"].mean()
REPORT = f"""Final report. Data: the cleaning pipeline (boilerplate removal, exact deduplication, quality rules, MinHash
near-deduplication and decontamination against the validation text) kept {len(kept)} of {len(raw_docs)} crawl documents,
{kept_kinds.count('leak')} leaked and {kept_kinds.count('junk')} junk among them, leaving {len(corpus):,} characters. Pretraining: a
{P['n_layer']}-layer GPT of width {P['d']} ({plan_params / 1e6:.1f} million parameters) trained for {P['steps']} steps,
{plan_tokens / 1e6:.1f} million tokens or {plan_tokens / len(corpus):.0f} passes over the cleaned corpus, which is the data-limited
regime the design document predicted; dropout {P['dropout']} and keeping the best checkpoint (step {best_step}) held the
validation loss at {pretrain_val:.3f} nats per byte. Fine-tuning: LoRA of rank {PLAN['sft']['rank']} ({sft_trainable:,} trainable
parameters, {PLAN['sft']['steps']} steps) took greedy accuracy on {len(test_words)} unseen words from {acc('pretrained', 'UPPER')} to
{acc('fine-tuned', 'UPPER')} on UPPER and from {acc('pretrained', 'REVERSE')} to {acc('fine-tuned', 'REVERSE')} on REVERSE, and moved the
validation loss from {STAGES['pretrained']['val']:.3f} to {STAGES['fine-tuned']['val']:.3f}. RL: {PLAN['rl']['steps']} steps against the exact
verifier on {rl_task}, with a KL weight of {PLAN['rl']['beta']}, changed sampled {rl_task} accuracy from
{acc('fine-tuned', rl_task, '_sampled')} to {acc('RL', rl_task, '_sampled')}, a paired change of {rl_gain[0]:+.3f}
[{rl_gain[1]:+.3f}, {rl_gain[2]:+.3f}]; greedy {rl_task} accuracy went from {acc('fine-tuned', rl_task)} to {acc('RL', rl_task)}, and UPPER,
which RL did not train, from {acc('fine-tuned', 'UPPER')} to {acc('RL', 'UPPER')}. Serving: with continuous batching the 95th
percentile gap between tokens was {serving['p95_itl_ms']:.1f} ms and time to first token {serving['p95_ttft_ms']:.1f} ms; {served_match:.0%} of
served answers matched full recomputation. The manifest chain from the raw crawl to the served outputs is
{'intact' if chain_break is None else 'broken'}. After fine-tuning, {harder} was the harder task ({STAGES['fine-tuned'][harder].mean():.2f} against
{STAGES['fine-tuned'][easier].mean():.2f} greedy), and sampling lost {sample_gap:.2f} of {rl_task} accuracy against greedy decoding, the gap RL
closed. With ten times the compute I would pretrain on a larger, deduplicated corpus
instead of repeating this one, so the model is no longer data-limited, and evaluate on more test words."""
# END SOLUTION
print(REPORT)
