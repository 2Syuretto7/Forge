# %% [markdown]
# # L22 capstone: an inference server that meets its targets
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. The notebook trains
# a small byte-level GPT on Tiny Shakespeare for a few minutes so there is a model to serve. You
# write the serving engine: prefill and decode with a key-value cache, a continuous-batching server
# loop over a fixed set of cache slots, and weight-only int8 quantization. Then you replay a
# workload of requests arriving over time, measure time to first token, inter-token latency and
# throughput, compare with serving one request at a time, and write the report. The last cell is
# the autograder; it prints a completion code to paste into the lesson.

# %%
import copy
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
# Exact float32 matmuls, so cached and uncached generation can be compared token by token.
torch.backends.cuda.matmul.allow_tf32 = False
torch.backends.cudnn.allow_tf32 = False

# %% [markdown]
# ## 1. Configuration and targets
#
# The server must beat serving one request at a time by `speedup` in throughput when every request
# is queued, and on the arriving workload keep the 95th percentile of the gap between consecutive
# tokens of a request under `p95_itl_ms` and the 95th percentile of the time from arrival to first
# token under `p95_ttft_ms`.

# %%
CFG = dict(d=384, n_layer=6, n_head=6, ctx=256, batch=32, steps=800, lr=2e-3, warmup=100,
           n_requests=64, rate=40.0, max_batch=32, prompt_len=(16, 96), new_tokens=(32, 128), seed=0)
TARGETS = dict(speedup=4.0, p95_itl_ms=50.0, p95_ttft_ms=500.0)
if SMALL:
    CFG.update(d=64, n_layer=2, n_head=2, ctx=64, batch=8, steps=30, n_requests=8, rate=50.0, max_batch=4,
               prompt_len=(8, 24), new_tokens=(8, 24))

CORPUS_URL = "https://raw.githubusercontent.com/karpathy/char-rnn/master/data/tinyshakespeare/input.txt"
CORPUS_SHA256 = "86c4e6aa9db7c042ec79f339dcb96d42b0075e16b8fc2e86bf0ca57e2dc565ed"
local = [p for p in (pathlib.Path("data/tinyshakespeare.txt"), pathlib.Path("../data/tinyshakespeare.txt")) if p.exists()]
raw_bytes = local[0].read_bytes() if local else urllib.request.urlopen(CORPUS_URL, timeout=60).read()
assert hashlib.sha256(raw_bytes).hexdigest() == CORPUS_SHA256, "unexpected corpus contents"
data = torch.tensor(list(raw_bytes), dtype=torch.long)
split = int(0.9 * len(data))
train_data, val_data = data[:split], data[split:]

# %% [markdown]
# ## 2. A model to serve
#
# The GPT of L14 at byte level, with the parts of each block exposed so the serving code can call
# them one at a time. Training takes about three minutes on a T4.

# %%
class Block(nn.Module):
    def __init__(self, d, n_head):
        super().__init__()
        self.d, self.n_head = d, n_head
        self.ln1, self.ln2 = nn.LayerNorm(d), nn.LayerNorm(d)
        self.qkv, self.proj = nn.Linear(d, 3 * d), nn.Linear(d, d)
        self.fc1, self.fc2 = nn.Linear(d, 4 * d), nn.Linear(4 * d, d)

    def heads(self, t):
        """(B, T, d) to (B, n_head, T, d_head)."""
        B, T, _ = t.shape
        return t.view(B, T, self.n_head, self.d // self.n_head).transpose(1, 2)

    def merge(self, t):
        """(B, n_head, T, d_head) to (B, T, d)."""
        B, _, T, _ = t.shape
        return t.transpose(1, 2).reshape(B, T, self.d)

    def mlp(self, x):
        return self.fc2(F.gelu(self.fc1(self.ln2(x))))

    def forward(self, x):
        q, k, v = (self.heads(t) for t in self.qkv(self.ln1(x)).split(self.d, dim=2))
        x = x + self.proj(self.merge(F.scaled_dot_product_attention(q, k, v, is_causal=True)))
        return x + self.mlp(x)


class GPT(nn.Module):
    def __init__(self, d, n_layer, n_head, ctx):
        super().__init__()
        self.d, self.n_head, self.ctx = d, n_head, ctx
        self.tok, self.pos = nn.Embedding(256, d), nn.Embedding(ctx, d)
        nn.init.normal_(self.tok.weight, std=0.02)
        nn.init.normal_(self.pos.weight, std=0.02)
        self.blocks = nn.ModuleList([Block(d, n_head) for _ in range(n_layer)])
        self.ln_f = nn.LayerNorm(d)

    def head(self, x):
        return self.ln_f(x) @ self.tok.weight.T

    def forward(self, idx):
        x = self.tok(idx) + self.pos(torch.arange(idx.shape[1], device=idx.device))
        for b in self.blocks:
            x = b(x)
        return self.head(x)


def batch_of(src, gen, n=None):
    ix = torch.randint(len(src) - CFG["ctx"] - 1, (n or CFG["batch"],), generator=gen)
    x = torch.stack([src[i:i + CFG["ctx"]] for i in ix])
    y = torch.stack([src[i + 1:i + CFG["ctx"] + 1] for i in ix])
    return x.to(DEVICE), y.to(DEVICE)


@torch.no_grad()
def val_loss(model, n=64):
    model.eval()
    x, y = batch_of(val_data, torch.Generator().manual_seed(1), n)
    loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten()).item()
    model.train()
    return loss


torch.manual_seed(CFG["seed"])
model = GPT(CFG["d"], CFG["n_layer"], CFG["n_head"], CFG["ctx"]).to(DEVICE)
opt = torch.optim.AdamW(model.parameters(), lr=CFG["lr"], betas=(0.9, 0.95), weight_decay=0.1)
gen = torch.Generator().manual_seed(0)
t0 = time.time()
for step in range(1, CFG["steps"] + 1):
    for group in opt.param_groups:
        group["lr"] = CFG["lr"] * min(1.0, step / CFG["warmup"]) * (0.1 + 0.45 * (1 + math.cos(math.pi * step / CFG["steps"])))
    x, y = batch_of(train_data, gen)
    loss = F.cross_entropy(model(x).flatten(0, 1), y.flatten())
    opt.zero_grad(set_to_none=True)
    loss.backward()
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    opt.step()
    if step % 200 == 0 or step == CFG["steps"]:
        print(f"step {step}: train loss {loss.item():.3f} ({time.time() - t0:.0f} s)")
model.eval()
base_val = val_loss(model)
n_params = sum(p.numel() for p in model.parameters())
print(f"{n_params:,} parameters, validation loss {base_val:.3f} nats per byte")


@torch.no_grad()
def generate_reference(model, prompt, n):
    """Greedy decoding that recomputes the whole sequence for every token: slow and plainly correct."""
    ids = torch.tensor([prompt], device=DEVICE)
    out = []
    for _ in range(n):
        nxt = int(model(ids)[0, -1].argmax())
        out.append(nxt)
        ids = torch.cat([ids, torch.tensor([[nxt]], device=DEVICE)], dim=1)
    return out


# %% [markdown]
# ## 3. Prefill and decode with a key-value cache
#
# The cache holds keys and values for `slots` sequences at once, each in its own slot, with
# `lengths[s]` positions filled. Write:
#
# - `prefill(model, cache, slot, prompt)`: run the prompt through the model in one pass, store
#   every layer's keys and values for its positions in the slot, set the slot's length, and return
#   the logits for the next token (a vector of 256).
# - `decode_step(model, cache, slots, tokens)`: one new token for each of several slots at once,
#   each at its own position. Store each token's keys and values at its slot's next position,
#   attend over that slot's filled positions only, advance the lengths, and return the next-token
#   logits, one row per slot.
#
# Hint: index the cache with a tensor of slots and a tensor of positions together, and build a
# boolean mask of shape (batch, 1, 1, positions) for `scaled_dot_product_attention`, where `True`
# means "may attend".

# %%
class KVCache:
    def __init__(self, model, slots, max_len):
        shape = (len(model.blocks), slots, model.n_head, max_len, model.d // model.n_head)
        self.k = torch.zeros(shape, device=DEVICE)
        self.v = torch.zeros(shape, device=DEVICE)
        self.lengths = torch.zeros(slots, dtype=torch.long, device=DEVICE)


@torch.no_grad()
def prefill(model, cache, slot, prompt):
    # BEGIN SOLUTION
    ids = torch.tensor([prompt], device=DEVICE)
    T = ids.shape[1]
    x = model.tok(ids) + model.pos(torch.arange(T, device=DEVICE))
    for layer, b in enumerate(model.blocks):
        q, k, v = (b.heads(t) for t in b.qkv(b.ln1(x)).split(b.d, dim=2))
        cache.k[layer, slot, :, :T] = k[0]
        cache.v[layer, slot, :, :T] = v[0]
        x = x + b.proj(b.merge(F.scaled_dot_product_attention(q, k, v, is_causal=True)))
        x = x + b.mlp(x)
    cache.lengths[slot] = T
    return model.head(x[0, -1])
    # END SOLUTION


@torch.no_grad()
def decode_step(model, cache, slots, tokens):
    # BEGIN SOLUTION
    s = torch.as_tensor(slots, device=DEVICE)
    pos = cache.lengths[s]
    width = int(pos.max()) + 1
    mask = (torch.arange(width, device=DEVICE)[None, :] <= pos[:, None])[:, None, None, :]
    x = (model.tok(torch.as_tensor(tokens, device=DEVICE)) + model.pos(pos))[:, None, :]
    for layer, b in enumerate(model.blocks):
        q, k, v = (b.heads(t) for t in b.qkv(b.ln1(x)).split(b.d, dim=2))
        cache.k[layer, s, :, pos] = k[:, :, 0]
        cache.v[layer, s, :, pos] = v[:, :, 0]
        K, V = cache.k[layer, s, :, :width], cache.v[layer, s, :, :width]
        x = x + b.proj(b.merge(F.scaled_dot_product_attention(q, K, V, attn_mask=mask)))
        x = x + b.mlp(x)
    cache.lengths[s] += 1
    return model.head(x[:, 0])
    # END SOLUTION


def generate_cached(model, prompt, n):
    cache = KVCache(model, 1, CFG["ctx"])
    out = [int(prefill(model, cache, 0, prompt).argmax())]
    while len(out) < n:
        out.append(int(decode_step(model, cache, [0], [out[-1]])[0].argmax()))
    return out


sample = list(val_data[:40].tolist())
check_n = 48 if not SMALL else 16
cached, reference = generate_cached(model, sample, check_n), generate_reference(model, sample, check_n)
print("cached generation matches recomputation:", cached == reference)
print(repr(bytes(sample + cached).decode("utf-8", errors="replace")))

# %% [markdown]
# ## 4. The workload
#
# `n_requests` requests arrive as a Poisson process at `rate` per second, each with a prompt cut
# from the validation text and a number of tokens to generate. Every request is decoded greedily,
# so its output is fully determined and can be checked against `generate_reference`.

# %%
def make_workload(cfg=CFG):
    rng = np.random.default_rng(cfg["seed"])
    arrivals = np.cumsum(rng.exponential(1.0 / cfg["rate"], cfg["n_requests"]))
    arrivals -= arrivals[0]
    requests = []
    for i, t in enumerate(arrivals):
        n_prompt = int(rng.integers(cfg["prompt_len"][0], cfg["prompt_len"][1] + 1))
        start = int(rng.integers(0, len(val_data) - n_prompt))
        requests.append(dict(id=i, arrival=float(t), prompt=val_data[start:start + n_prompt].tolist(),
                             max_new=int(rng.integers(cfg["new_tokens"][0], cfg["new_tokens"][1] + 1))))
    return requests


requests = make_workload()
print(f"{len(requests)} requests over {requests[-1]['arrival']:.2f} s, "
      f"{sum(r['max_new'] for r in requests):,} tokens to generate")

# %% [markdown]
# ## 5. The server loop
#
# Write `serve(model, requests, max_batch)`, a continuous-batching loop with `max_batch` cache
# slots. Time runs from the start of the call; a request may be admitted only once its arrival
# time has passed. Repeat until every request is finished:
#
# 1. Admit arrived requests while slots are free: prefill each into a free slot and take its
#    first token, recording the time.
# 2. If no request is active, wait for the next arrival.
# 3. Otherwise run one `decode_step` over all active slots, append each slot's next token and
#    record the time; free the slot of every request that has `max_new` tokens.
#
# Return one record per request, in the order of `requests`, with keys `id`, `arrival`,
# `tokens` (the generated tokens) and `times` (the time at which each token was produced, in
# seconds from the start).

# %%
def serve(model, requests, max_batch):
    # BEGIN SOLUTION
    cache = KVCache(model, max_batch, CFG["ctx"])
    queue = sorted(requests, key=lambda r: r["arrival"])
    free, active, done = list(range(max_batch))[::-1], {}, {}
    start, i = time.perf_counter(), 0

    def now():
        return time.perf_counter() - start

    while i < len(queue) or active:
        while i < len(queue) and free and queue[i]["arrival"] <= now():
            r = queue[i]
            i += 1
            slot = free.pop()
            first = int(prefill(model, cache, slot, r["prompt"]).argmax())
            rec = dict(id=r["id"], arrival=r["arrival"], tokens=[first], times=[now()])
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
    # END SOLUTION


# %% [markdown]
# ## 6. Measure
#
# `metrics` summarizes a run: time to first token (from arrival), the gaps between consecutive
# tokens of each request, and throughput (generated tokens divided by the time from the first
# arrival to the last token). Latency is measured on the workload as it arrives. Throughput is
# compared at saturation, with every request queued at time zero, so that it measures the server
# rather than the arrival rate: continuous batching against serving one request at a time
# (`max_batch=1`).

# %%
def metrics(records):
    ttft = np.array([r["times"][0] - r["arrival"] for r in records])
    itl = np.concatenate([np.diff(r["times"]) for r in records if len(r["times"]) > 1])
    span = max(r["times"][-1] for r in records) - min(r["arrival"] for r in records)
    return dict(throughput=sum(len(r["tokens"]) for r in records) / span,
                p50_ttft_ms=1e3 * float(np.percentile(ttft, 50)), p95_ttft_ms=1e3 * float(np.percentile(ttft, 95)),
                p50_itl_ms=1e3 * float(np.percentile(itl, 50)), p95_itl_ms=1e3 * float(np.percentile(itl, 95)))


def show(name, m):
    print(f"{name:>10}: {m['throughput']:7.0f} tokens/s, first token p50 {m['p50_ttft_ms']:6.1f} ms "
          f"p95 {m['p95_ttft_ms']:7.1f} ms, between tokens p50 {m['p50_itl_ms']:5.1f} ms p95 {m['p95_itl_ms']:5.1f} ms")


serve(model, requests[: min(4, len(requests))], CFG["max_batch"])
records = serve(model, requests, CFG["max_batch"])
batched = metrics(records)
show("arriving", batched)
queued = [dict(r, arrival=0.0) for r in requests]
saturated = metrics(serve(model, queued, CFG["max_batch"]))
one_at_a_time = metrics(serve(model, queued, 1))
show("all queued", saturated)
show("one by one", one_at_a_time)
speedup = saturated["throughput"] / one_at_a_time["throughput"]
print(f"speedup at saturation {speedup:.1f}x")

reference_outputs = [generate_reference(model, r["prompt"], r["max_new"]) for r in requests]
served_match = float(np.mean([rec["tokens"] == ref for rec, ref in zip(records, reference_outputs)]))
print(f"{served_match:.0%} of served requests match recomputation exactly")
for name, target in TARGETS.items():
    value = speedup if name == "speedup" else batched[name]
    ok = value >= target if name == "speedup" else value <= target
    print(f"target {name}: {value:.1f} against {target} -> {'met' if ok else 'MISSED'}")

# %% [markdown]
# ## 7. Weight-only int8
#
# Write `quantize_int8(W)`: symmetric per-row quantization, returning int8 values `q` and one
# float32 scale per row with `W` approximately `q * scale[:, None]`; and `Int8Linear.forward`,
# which dequantizes on the fly. `quantize_model` swaps every linear layer in the blocks. Storing
# int8 weights cuts the bytes a decode step must read by four against float32; turning that into
# speed needs a fused kernel that dequantizes as it loads (L12), so here we measure size and quality.

# %%
def quantize_int8(W):
    # BEGIN SOLUTION
    scale = W.abs().amax(dim=1).clamp_min(1e-12) / 127.0
    q = torch.round(W / scale[:, None]).clamp(-127, 127).to(torch.int8)
    return q, scale.float()
    # END SOLUTION


class Int8Linear(nn.Module):
    def __init__(self, linear):
        super().__init__()
        q, scale = quantize_int8(linear.weight.data)
        self.register_buffer("q", q)
        self.register_buffer("scale", scale)
        self.bias = linear.bias

    def forward(self, x):
        # BEGIN SOLUTION
        return F.linear(x, self.q.to(x.dtype) * self.scale[:, None].to(x.dtype), self.bias)
        # END SOLUTION


def quantize_model(model):
    qm = copy.deepcopy(model)
    for b in qm.blocks:
        for name in ["qkv", "proj", "fc1", "fc2"]:
            setattr(b, name, Int8Linear(getattr(b, name)))
    return qm


def linear_weight_bytes(m):
    total = 0
    for b in m.blocks:
        for name in ["qkv", "proj", "fc1", "fc2"]:
            layer = getattr(b, name)
            total += layer.q.numel() + 4 * layer.scale.numel() if isinstance(layer, Int8Linear) else 4 * layer.weight.numel()
    return total


qmodel = quantize_model(model)
int8_val = val_loss(qmodel)
agree = []
for r in requests[:16]:
    a, b = generate_cached(model, r["prompt"], 32), generate_cached(qmodel, r["prompt"], 32)
    agree.append(np.mean([x == y for x, y in zip(a, b)]))
int8_agreement = float(np.mean(agree))
bytes_fp32, bytes_int8 = linear_weight_bytes(model), linear_weight_bytes(qmodel)
print(f"linear weights {bytes_fp32 / 1e6:.1f} MB in float32, {bytes_int8 / 1e6:.1f} MB in int8; "
      f"validation loss {base_val:.4f} -> {int8_val:.4f}; greedy tokens agree {int8_agreement:.0%}")

# %% [markdown]
# ## 8. Report
#
# In `REPORT`, write at least 80 words: the model and workload, the throughput and latency of the
# batched server against one-at-a-time serving and the targets, why batching helps decode, and what
# int8 did to size and quality.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
REPORT = f"""Serving report. A {CFG['n_layer']}-layer byte-level GPT of width {CFG['d']} ({n_params / 1e6:.1f} million parameters,
validation loss {base_val:.3f}) served {len(requests)} requests arriving at {CFG['rate']:.0f} per second, greedy decoding,
with continuous batching over {CFG['max_batch']} key-value cache slots. As the requests arrived, the 95th percentile
inter-token latency was {batched['p95_itl_ms']:.1f} ms and the 95th percentile time to first token {batched['p95_ttft_ms']:.1f} ms, against targets
of {TARGETS['p95_itl_ms']:.0f} ms and {TARGETS['p95_ttft_ms']:.0f} ms. With every request queued, the server reached a throughput of
{saturated['throughput']:.0f} tokens per second against {one_at_a_time['throughput']:.0f} serving one request at a time, a speedup of {speedup:.1f}x.
Batching helps because a decode step reads every weight once whatever the batch size, so each extra sequence adds little
time until the step becomes compute-bound; one at a time, requests queue behind each other and the median first-token
time grows to {one_at_a_time['p50_ttft_ms'] / 1e3:.1f} s. {served_match:.0%} of the
served outputs matched full recomputation token for token. Int8 weight-only quantization with per-row scales cut the linear
weights from {bytes_fp32 / 1e6:.1f} MB to {bytes_int8 / 1e6:.1f} MB, moved the validation loss from {base_val:.4f} to {int8_val:.4f}, and
kept {int8_agreement:.0%} of greedy tokens unchanged; a fused dequantizing kernel would turn the smaller weights into faster steps."""
# END SOLUTION
print(REPORT)
