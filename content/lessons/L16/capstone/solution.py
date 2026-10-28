# %% [markdown]
# # L16 capstone: clean a crawl, then prove it helped
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. You get a noisy
# "crawl" built from Tiny Shakespeare: the plays cut into documents, plus exact and near copies,
# boilerplate footers, junk pages and copies of part of the validation set. You write the cleaning
# pipeline (exact deduplication, boilerplate removal, quality rules, MinHash near-deduplication and
# decontamination), then train the same small byte-level GPT for the same number of steps on the raw
# and on the cleaned crawl, and compare them on held-out text that never leaked. The last cell is
# the autograder; it prints a completion code to paste into the lesson.

# %%
import hashlib
import math
import os
import pathlib
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

# %% [markdown]
# ## 1. The corpus and three splits
#
# The first 80% of the text is the source of training documents. The next 10% is a **validation**
# set, part of which leaks into the crawl, as benchmark questions leak onto the web. The last 10%
# is a **test** set that never leaks.

# %%
CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
CORPUS_SHA256 = "86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed"
local = [p for p in (pathlib.Path("data/tinyshakespeare.txt"), pathlib.Path("../data/tinyshakespeare.txt")) if p.exists()]
raw_bytes = local[0].read_bytes() if local else urllib.request.urlopen(CORPUS_URL, timeout=60).read()
assert hashlib.sha256(raw_bytes).hexdigest() == CORPUS_SHA256, "unexpected corpus contents"
text = raw_bytes.decode("utf-8")
n = len(text)
train_text, val_text, test_text = text[: int(0.8 * n)], text[int(0.8 * n): int(0.9 * n)], text[int(0.9 * n):]


def chunk_docs(t, size=1000):
    """Cut text at blank lines into documents of about `size` characters."""
    docs, cur = [], ""
    for block in t.split("\n\n"):
        cur += block + "\n\n"
        if len(cur) >= size:
            docs.append(cur.strip())
            cur = ""
    if cur.strip():
        docs.append(cur.strip())
    return docs


source_docs = chunk_docs(train_text)
val_docs = chunk_docs(val_text)
print(f"{len(source_docs)} source documents, {len(val_docs)} validation documents")

# %% [markdown]
# ## 2. The crawl
#
# `make_crawl` builds the raw crawl deterministically. It also returns each document's kind and the
# source document it came from (-1 for junk and leaked text), which only the autograder uses to
# check your pipeline; do not use them in your code.

# %%
FOOTER = "Share this page: Facebook | Twitter | Email | Print"
SPAM = "buy cheap free best deal online discount offer click now win prize casino bonus".split()


def make_crawl(seed=0):
    rng = np.random.default_rng(seed)

    def perturb(doc, rate):
        w = doc.split(" ")
        for i in range(len(w)):
            if rng.random() < rate:
                w[i] = w[rng.integers(len(w))]
        return " ".join(w)

    crawl = []
    for i, d in enumerate(source_docs):
        crawl.append((d + ("\n" + FOOTER if rng.random() < 0.6 else ""), "source", i))
    for i in rng.choice(len(source_docs), len(source_docs) // 10, replace=False):
        for _ in range(10):
            d = source_docs[i]
            crawl.append((d.upper() if rng.random() < 0.3 else d.replace("\n", "\n "), "exact", int(i)))
    for i in rng.choice(len(source_docs), len(source_docs) // 10, replace=False):
        for _ in range(3):
            crawl.append((perturb(source_docs[i], 0.03), "near", int(i)))
    for _ in range(len(source_docs) // 4):
        kind = rng.integers(3)
        if kind == 0:
            junk = " ".join(rng.choice(SPAM, 200))
        elif kind == 1:
            junk = "\n".join(" | ".join(str(v) for v in rng.integers(0, 10000, 6)) for _ in range(40))
        else:
            junk = bytes(rng.integers(33, 127, 1000).tolist()).decode("ascii")
        crawl.append((junk, "junk", -1))
    leaked = sorted(rng.choice(len(val_docs), len(val_docs) // 10, replace=False).tolist())
    for i in leaked:
        for _ in range(40):
            crawl.append((val_docs[i], "leak", -1))
    order = rng.permutation(len(crawl))
    return [crawl[i][0] for i in order], [crawl[i][1] for i in order], [crawl[i][2] for i in order], leaked


raw_docs, kinds, origins, leaked_val = make_crawl()
print(f"{len(raw_docs)} crawl documents, {sum(map(len, raw_docs)):,} characters")
print({k: kinds.count(k) for k in sorted(set(kinds))})

# %% [markdown]
# ## 3. Exact duplicates and boilerplate
#
# Write `exact_dedup(docs)`, the indices of the first occurrence of each document after
# normalizing case and whitespace (compare SHA-1 digests), and `strip_boilerplate(docs, min_docs)`,
# which removes every line that occurs in at least `min_docs` different documents.

# %%
def normalize(doc):
    return " ".join(doc.lower().split())


def exact_dedup(docs):
    # BEGIN SOLUTION
    seen, keep = set(), []
    for i, d in enumerate(docs):
        h = hashlib.sha1(normalize(d).encode("utf-8")).hexdigest()
        if h not in seen:
            seen.add(h)
            keep.append(i)
    return keep
    # END SOLUTION


def strip_boilerplate(docs, min_docs):
    # BEGIN SOLUTION
    counts = {}
    for d in docs:
        for line in {l.strip() for l in d.split("\n") if l.strip()}:
            counts[line] = counts.get(line, 0) + 1
    common = {line for line, c in counts.items() if c >= min_docs}
    return ["\n".join(l for l in d.split("\n") if l.strip() not in common) for d in docs]
    # END SOLUTION


# %% [markdown]
# ## 4. Quality rules
#
# Write `passes_quality(doc)` with the Gopher rules from exercise 6: 50 to 100,000 words, mean word
# length 3 to 10, at most 0.1 `#` or `...` per word, at least 80% of words containing a letter, and
# at least two of the stop words.

# %%
STOP_WORDS = {"the", "be", "to", "of", "and", "that", "have", "with"}


def passes_quality(doc):
    # BEGIN SOLUTION
    words = doc.split()
    if not 50 <= len(words) <= 100_000:
        return False
    mean_len = sum(map(len, words)) / len(words)
    alpha = sum(any(c.isalpha() for c in w) for w in words) / len(words)
    stops = {w.strip(".,;:!?\"'()").lower() for w in words} & STOP_WORDS
    symbols = max(doc.count("#"), doc.count("...")) / len(words)
    return 3 <= mean_len <= 10 and alpha >= 0.8 and len(stops) >= 2 and symbols <= 0.1
    # END SOLUTION


# %% [markdown]
# ## 5. Near duplicates with MinHash and LSH
#
# Write `minhash(doc, a, b)`: the signature of the document's character 5-gram shingles (after
# `normalize`), hashed with CRC-32 and then with $h_i(x) = (a_i x + b_i) \bmod (2^{31} - 1)$. Then
# write `near_dedup(signatures, bands, rows, min_similarity)`, returning the sorted positions to
# keep: put each band in a bucket, confirm every pair sharing a bucket by its signature agreement
# rate, join confirmed pairs with union-find and keep the smallest position of each cluster.

# %%
PRIME = 2 ** 31 - 1
NUM_PERM, BANDS, ROWS = 128, 16, 8
_hrng = np.random.default_rng(1)
HASH_A, HASH_B = _hrng.integers(1, PRIME, NUM_PERM), _hrng.integers(0, PRIME, NUM_PERM)


def minhash(doc, a=HASH_A, b=HASH_B):
    # BEGIN SOLUTION
    t = normalize(doc)
    sh = {t[i:i + 5] for i in range(len(t) - 4)} or {t}
    x = np.array(sorted(zlib.crc32(s.encode("utf-8")) for s in sh), dtype=np.int64) % PRIME
    return ((np.outer(a, x) + b[:, None]) % PRIME).min(axis=1)
    # END SOLUTION


def near_dedup(signatures, bands=BANDS, rows=ROWS, min_similarity=0.7):
    # BEGIN SOLUTION
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
    # END SOLUTION


# %% [markdown]
# ## 6. Decontamination
#
# Write `decontaminate(docs, eval_docs, n=13)`: the positions of the documents that share no
# 13-word sequence with any validation document (words lowercased, surrounding punctuation
# stripped, as in exercise 9).

# %%
def words_of(doc):
    return [w for w in (x.strip(".,;:!?\"'()[]").lower() for x in doc.split()) if w]


def decontaminate(docs, eval_docs, n=13):
    # BEGIN SOLUTION
    index = set()
    for d in eval_docs:
        w = words_of(d)
        index |= {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}
    keep = []
    for j, d in enumerate(docs):
        w = words_of(d)
        if not any(tuple(w[i:i + n]) in index for i in range(len(w) - n + 1)):
            keep.append(j)
    return keep
    # END SOLUTION


# %% [markdown]
# ## 7. The pipeline
#
# Run the steps in order, keeping track of which crawl documents survive. Boilerplate goes first,
# so that a page and its copy without the footer become exact duplicates.

# %%
t0 = time.time()
cleaned = strip_boilerplate(raw_docs, min_docs=50)
kept = exact_dedup(cleaned)
kept = [i for i in kept if passes_quality(cleaned[i])]
signatures = [minhash(cleaned[i]) for i in kept]
kept = [kept[j] for j in near_dedup(signatures)]
kept = [kept[j] for j in decontaminate([cleaned[i] for i in kept], val_docs)]
clean_docs = [cleaned[i] for i in kept]
kept_kinds = [kinds[i] for i in kept]
kept_origins = [origins[i] for i in kept]
print(f"pipeline: {time.time() - t0:.0f} s; kept {len(clean_docs)} of {len(raw_docs)} documents")
for k in sorted(set(kinds)):
    print(f"  {k:7s}: kept {kept_kinds.count(k):5d} of {kinds.count(k):5d}")
raw_corpus = "\n\n".join(raw_docs)
clean_corpus = "\n\n".join(clean_docs)
print(f"{len(raw_corpus):,} characters before, {len(clean_corpus):,} after")

# %% [markdown]
# ## 8. Equal compute, two datasets
#
# The same byte-level GPT, trained for the same number of steps (so the same compute and the same
# number of tokens) on each corpus. Each is scored on the test split, which never leaked, and on the
# leaked and unleaked parts of the validation split.

# %%
CFG = dict(ctx=128, batch=16, d=128, n_layer=4, n_head=4, steps=800, lr=3e-3, warmup=100)
if SMALL:
    CFG.update(ctx=32, batch=8, d=32, n_layer=1, n_head=2, steps=60, lr=3e-3, warmup=10)
CTX = CFG["ctx"]


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
        x = x + self.proj(F.scaled_dot_product_attention(q, k, v, is_causal=True).transpose(1, 2).reshape(B, T, d))
        return x + self.mlp(self.ln2(x))


class GPT(nn.Module):
    def __init__(self, d, n_layer, n_head):
        super().__init__()
        self.tok, self.pos = nn.Embedding(256, d), nn.Embedding(CTX, d)
        nn.init.normal_(self.tok.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)
        self.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)

    def forward(self, idx):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device))
        for b in self.blocks:
            x = b(x)
        return self.ln_f(x) @ self.tok.weight.T


def encode(t):
    return torch.tensor(list(t.encode("utf-8")), dtype=torch.long)


@torch.no_grad()
def loss_on(model, t):
    model.eval()
    ids = encode(t)
    n = (len(ids) - 1) // CTX
    x, y = ids[: n * CTX].view(n, CTX), ids[1: n * CTX + 1].view(n, CTX)
    total = 0.0
    for i in range(0, n, 256):
        logits = model(x[i:i + 256].to(DEVICE))
        total += F.cross_entropy(logits.flatten(0, 1), y[i:i + 256].to(DEVICE).flatten(), reduction="sum").item()
    model.train()
    return total / (n * CTX)


def train_on(corpus):
    torch.manual_seed(0)
    ids = encode(corpus)
    model = GPT(CFG["d"], CFG["n_layer"], CFG["n_head"]).to(DEVICE)
    opt = torch.optim.AdamW(model.parameters(), lr=CFG["lr"], betas=(0.9, 0.95), weight_decay=0.1)
    gen = torch.Generator().manual_seed(0)
    for step in range(1, CFG["steps"] + 1):
        for group in opt.param_groups:
            group["lr"] = CFG["lr"] * min(1.0, step / CFG["warmup"]) * (0.1 + 0.45 * (1 + math.cos(math.pi * step / CFG["steps"])))
        ix = torch.randint(len(ids) - CTX - 1, (CFG["batch"],), generator=gen)
        x = torch.stack([ids[i:i + CTX] for i in ix]).to(DEVICE)
        y = torch.stack([ids[i + 1:i + CTX + 1] for i in ix]).to(DEVICE)
        loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
        opt.zero_grad(set_to_none=True)
        loss.backward()
        torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
        opt.step()
    return model


leaked_text = "\n\n".join(val_docs[i] for i in leaked_val)
unleaked_text = "\n\n".join(d for i, d in enumerate(val_docs) if i not in set(leaked_val))
results = {}
for name, corpus in [("raw", raw_corpus), ("clean", clean_corpus)]:
    t0 = time.time()
    model = train_on(corpus)
    results[name] = {"test": loss_on(model, test_text), "leaked": loss_on(model, leaked_text), "unleaked": loss_on(model, unleaked_text)}
    print(name, {k: round(v, 4) for k, v in results[name].items()}, f"({time.time() - t0:.0f} s)")

# %% [markdown]
# ## 9. Report
#
# In `REPORT`, write at least 80 words: what each step removed, the test-loss difference between
# the two models, and what the leaked and unleaked validation losses show about contamination.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
gain = results["raw"]["test"] - results["clean"]["test"]
REPORT = f"""The crawl had {len(raw_docs)} documents; the pipeline kept {len(clean_docs)}. Exact deduplication removed the
copies that differed only in case and spacing, the boilerplate step stripped the shared footer, the quality rules
removed {kinds.count('junk') - kept_kinds.count('junk')} of {kinds.count('junk')} junk pages, MinHash with LSH removed the near copies,
and decontamination removed every document containing validation text. At equal compute the model trained on the
cleaned crawl reached a test loss of {results['clean']['test']:.3f} nats per byte against {results['raw']['test']:.3f}
for the raw crawl, a gain of {gain:.3f}. The raw model scored {results['raw']['leaked']:.3f} on the leaked validation
documents and {results['raw']['unleaked']:.3f} on the unleaked ones: contamination makes a model look better exactly
where it memorized, so the leaked part of the validation set no longer measures generalization."""
# END SOLUTION
print(REPORT)
