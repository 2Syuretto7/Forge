# %% [markdown]
# # L14 capstone: a GPT with its own tokenizer
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. You will train a
# byte-level BPE tokenizer on Shakespeare, encode the corpus, train a small GPT on the tokens, measure
# its validation loss in bits per character (comparable across tokenizers), and sample from it with
# temperature, top-k and top-p. The last cell is the autograder.

# %%
import hashlib
import math
import os
import pathlib
import re
import time
import urllib.request

import torch
import torch.nn as nn
import torch.nn.functional as F

SMALL = os.environ.get("SMALL") == "1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
torch.manual_seed(0)

CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
CORPUS_SHA256 = "86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed"
# Inside a checkout of the Forge repository the file is already there; in Colab it is downloaded.
local = [p for p in (pathlib.Path("data/tinyshakespeare.txt"), pathlib.Path("../data/tinyshakespeare.txt")) if p.exists()]
raw = local[0].read_bytes() if local else urllib.request.urlopen(CORPUS_URL, timeout=60).read()
assert hashlib.sha256(raw).hexdigest() == CORPUS_SHA256, "unexpected corpus contents"
text = raw.decode("utf-8")
if SMALL:
    text = text[:60_000]
split_at = int(0.9 * len(text))
train_text, val_text = text[:split_at], text[split_at:]
print(f"{len(text):,} characters; device {DEVICE}")

# %% [markdown]
# ## 1. A byte-level BPE tokenizer
#
# Split the text into chunks with the pattern below (words keep their leading space), count each
# distinct chunk once with its frequency, and learn merges of the most frequent adjacent pair within
# chunks, starting from the 256 byte values. Encode by applying merges in the order they were learned.

# %%
PATTERN = re.compile(r"'s|'t|'re|'ve|'m|'ll|'d| ?[^\W\d_]+| ?\d+| ?[^\s\w]+|\s+(?!\S)|\s+")
VOCAB_SIZE = 300 if SMALL else 512


def merge(ids, pair, new_id):
    out, i = [], 0
    while i < len(ids):
        if i + 1 < len(ids) and ids[i] == pair[0] and ids[i + 1] == pair[1]:
            out.append(new_id)
            i += 2
        else:
            out.append(ids[i])
            i += 1
    return out


def train_bpe(text, vocab_size):
    """Return the merges {(a, b): new_id} in the order learned."""
    # BEGIN SOLUTION
    freq = {}
    for c in PATTERN.findall(text):
        freq[c] = freq.get(c, 0) + 1
    words = {c: list(c.encode("utf-8")) for c in freq}
    merges = {}
    for new_id in range(256, vocab_size):
        counts = {}
        for c, ids in words.items():
            for p in zip(ids, ids[1:]):
                counts[p] = counts.get(p, 0) + freq[c]
        if not counts:
            break
        best = max(counts, key=counts.get)
        if counts[best] < 2:
            break
        words = {c: (merge(ids, best, new_id) if len(ids) > 1 else ids) for c, ids in words.items()}
        merges[best] = new_id
    return merges
    # END SOLUTION


class Tokenizer:
    def __init__(self, merges):
        self.merges = merges
        self.vocab = {i: bytes([i]) for i in range(256)}
        for (a, b), i in merges.items():
            self.vocab[i] = self.vocab[a] + self.vocab[b]
        self.cache = {}

    def encode_chunk(self, chunk):
        if chunk not in self.cache:
            # BEGIN SOLUTION
            ids = list(chunk.encode("utf-8"))
            while len(ids) >= 2:
                pairs = set(zip(ids, ids[1:]))
                best = min(pairs, key=lambda p: self.merges.get(p, float("inf")))
                if best not in self.merges:
                    break
                ids = merge(ids, best, self.merges[best])
            self.cache[chunk] = ids
            # END SOLUTION
        return self.cache[chunk]

    def encode(self, text):
        return [i for chunk in PATTERN.findall(text) for i in self.encode_chunk(chunk)]

    def decode(self, ids):
        return b"".join(self.vocab[i] for i in ids).decode("utf-8", errors="replace")


t0 = time.time()
tok = Tokenizer(train_bpe(train_text, VOCAB_SIZE))
train_ids = torch.tensor(tok.encode(train_text), dtype=torch.long)
val_ids = torch.tensor(tok.encode(val_text), dtype=torch.long)
chars_per_token = len(val_text) / len(val_ids)
print(f"tokenizer trained in {time.time() - t0:.0f} s; {chars_per_token:.2f} characters per token on validation text")
print([tok.vocab[i] for i in range(256, 266)])

# %% [markdown]
# ## 2. The model
#
# The same pre-norm GPT as in L13 (paste your own if you prefer), with the output layer tied to the
# token embedding.

# %%
class Block(nn.Module):
    def __init__(self, d, n_head):
        super().__init__()
        self.n_head = n_head
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv, self.proj = nn.Linear(d, 3 * d), nn.Linear(d, d)
        self.mlp = nn.Sequential(nn.Linear(d, 4 * d), nn.GELU(), nn.Linear(4 * d, d))

    def attn(self, x):
        B, T, d = x.shape
        q, k, v = self.qkv(x).split(d, dim=2)
        q, k, v = (t.view(B, T, self.n_head, d // self.n_head).transpose(1, 2) for t in (q, k, v))
        y = F.scaled_dot_product_attention(q, k, v, is_causal=True)
        return self.proj(y.transpose(1, 2).reshape(B, T, d))

    def forward(self, x):
        x = x + self.attn(self.ln1(x))
        return x + self.mlp(self.ln2(x))


class GPT(nn.Module):
    def __init__(self, vocab, ctx, d, n_layer, n_head):
        super().__init__()
        self.ctx = ctx
        self.tok = nn.Embedding(vocab, d)
        self.pos = nn.Embedding(ctx, d)
        self.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)
        # Small embeddings (as in GPT-2): with tied weights, N(0, 1) entries would make the initial
        # logits huge.
        nn.init.normal_(self.tok.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)

    def forward(self, idx):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device))
        for b in self.blocks:
            x = b(x)
        return self.ln_f(x) @ self.tok.weight.T


# %% [markdown]
# ## 3. Training with evaluation
#
# Write `estimate_loss`, the mean cross-entropy (nats per token) over `batches` random validation
# windows drawn with a fixed seed, in evaluation mode and without gradients.

# %%
CFG = dict(ctx=128, d=192, n_layer=4, n_head=6, batch=32, steps=1500, lr=2e-3, warmup=100)
if SMALL:
    CFG.update(ctx=32, d=32, n_layer=1, n_head=2, batch=8, steps=120, lr=3e-3, warmup=10)


def get_batch(ids, gen):
    ix = torch.randint(len(ids) - CFG["ctx"] - 1, (CFG["batch"],), generator=gen)
    x = torch.stack([ids[i:i + CFG["ctx"]] for i in ix])
    y = torch.stack([ids[i + 1:i + CFG["ctx"] + 1] for i in ix])
    return x.to(DEVICE), y.to(DEVICE)


@torch.no_grad()
def estimate_loss(model, ids, batches=20, seed=1):
    # BEGIN SOLUTION
    model.eval()
    g = torch.Generator().manual_seed(seed)
    total = 0.0
    for _ in range(batches):
        x, y = get_batch(ids, g)
        total += F.cross_entropy(model(x).flatten(0, 1), y.flatten()).item()
    model.train()
    return total / batches
    # END SOLUTION


model = GPT(len(tok.vocab), CFG["ctx"], CFG["d"], CFG["n_layer"], CFG["n_head"]).to(DEVICE)
opt = torch.optim.AdamW(model.parameters(), lr=CFG["lr"], weight_decay=0.1)
gen = torch.Generator().manual_seed(0)
history = []
t0 = time.time()
for step in range(1, CFG["steps"] + 1):
    lr = CFG["lr"] * min(1.0, step / CFG["warmup"]) * 0.5 * (1.0 + math.cos(math.pi * step / CFG["steps"]))
    for group in opt.param_groups:
        group["lr"] = lr
    x, y = get_batch(train_ids, gen)
    loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
    opt.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    if step == 1 or step % max(1, CFG["steps"] // 10) == 0:
        history.append((step, loss.item(), estimate_loss(model, val_ids, batches=5)))
        print(f"step {step}: train {history[-1][1]:.3f}, val {history[-1][2]:.3f} nats/token ({time.time() - t0:.0f} s)")

val_nats_per_token = estimate_loss(model, val_ids)
val_bits_per_char = val_nats_per_token / chars_per_token / math.log(2)
print(f"validation: {val_nats_per_token:.3f} nats per token = {val_bits_per_char:.3f} bits per character")

# %% [markdown]
# ## 4. Sampling
#
# Write `filter_logits(logits, top_k, top_p)` for a 1-D tensor of logits: keep the `top_k` largest
# (if given), then the smallest set of tokens, in order of probability, whose total probability reaches
# `top_p` (if given), setting everything else to `-inf`. `generate` applies the temperature first.

# %%
def filter_logits(logits, top_k=None, top_p=None):
    # BEGIN SOLUTION
    logits = logits.clone()
    if top_k is not None and top_k < logits.numel():
        cut = torch.topk(logits, top_k).values[-1]
        logits[logits < cut] = float("-inf")
    if top_p is not None:
        probs, order = torch.sort(torch.softmax(logits, dim=-1), descending=True)
        keep = int(torch.searchsorted(torch.cumsum(probs, dim=-1), torch.tensor(top_p, device=probs.device))) + 1
        drop = order[keep:]
        logits[drop] = float("-inf")
    return logits
    # END SOLUTION


@torch.no_grad()
def generate(prompt, n_tokens, temperature=1.0, top_k=None, top_p=None, seed=0):
    model.eval()
    g = torch.Generator(device=DEVICE).manual_seed(seed)
    idx = torch.tensor([tok.encode(prompt)], device=DEVICE)
    for _ in range(n_tokens):
        logits = model(idx[:, -CFG["ctx"]:])[0, -1] / temperature
        probs = torch.softmax(filter_logits(logits, top_k, top_p), dim=-1)
        idx = torch.cat([idx, torch.multinomial(probs, 1, generator=g)[None]], dim=1)
    model.train()
    return tok.decode(idx[0].tolist())


samples = {T: generate("ROMEO:\n", 120, temperature=T, top_p=0.9) for T in (0.5, 1.0)}
for T, s in samples.items():
    print(f"--- temperature {T}, top-p 0.9 ---\n{s}\n")

# %% [markdown]
# ## 5. Report
#
# At least 80 words: your tokenizer's vocabulary size and characters per token, the model and training
# settings, the validation loss in nats per token and in bits per character, and what changes in the
# samples between the two temperatures.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
REPORT = f"""
The tokenizer is byte-level BPE with a vocabulary of {len(tok.vocab)} (256 bytes and {len(tok.merges)}
merges learned within whitespace-delimited chunks), and it averages {chars_per_token:.2f} characters per
token on the validation text. The model is a pre-norm GPT with {CFG['n_layer']} layers of width {CFG['d']},
{CFG['n_head']} heads, a context of {CFG['ctx']} tokens and tied input and output embeddings, trained with
AdamW at a peak learning rate of {CFG['lr']} with warmup and cosine decay for {CFG['steps']} steps of
{CFG['batch']} windows. Its validation loss is {val_nats_per_token:.3f} nats per token, which is
{val_bits_per_char:.3f} bits per character once divided by the characters per token. At temperature 0.5
the samples are conservative and repeat common names and phrases; at temperature 1.0 with top-p 0.9 they
use more varied words but drift into invented ones and lose the thread sooner.
"""
# END SOLUTION
