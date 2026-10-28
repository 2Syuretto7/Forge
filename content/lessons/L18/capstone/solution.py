# %% [markdown]
# # L18 capstone: plan a run, then simulate it
#
# This notebook runs on any runtime; the CPU runtime is enough. Part 1 plans the parallel layout of
# a 13-billion-parameter model on 64 GPUs. Part 2 starts four processes on this machine, joined by
# `torch.distributed` with the gloo backend, and implements the communication of that plan: ring
# collectives from point-to-point messages, data parallelism, ZeRO stage 1 and a tensor-parallel
# MLP, each checked against a single-process reference. The last cell is the autograder; it prints
# a completion code to paste into the lesson.

# %%
import math
import os
import socket
import traceback
from datetime import timedelta

import torch
import torch.distributed as dist
import torch.multiprocessing as mp
import torch.nn as nn
import torch.nn.functional as F

SMALL = os.environ.get("SMALL") == "1"
WORLD = 4
torch.manual_seed(0)

# %% [markdown]
# ## Part 1. The plan
#
# The model has 40 layers of width 5120 with 40 heads, sequence length 2048, and is trained with a
# global batch of 1024 sequences (about 2 million tokens). The cluster has 64 GPUs of 80 GB in 8
# servers; NVLink connects the 8 GPUs inside a server, a slower network connects the servers.
# `memory_per_gpu` is the planner's formula (FlashAttention, 1F1B pipeline schedule).

# %%
MODEL = dict(layers=40, d=5120, heads=40, vocab=50257)
N_GPUS, GPU_BYTES, NODE_SIZE, SEQ, GLOBAL_SEQS = 64, 80 * 2 ** 30, 8, 2048, 1024


def params(m):
    return 12 * m["layers"] * m["d"] ** 2 + m["vocab"] * m["d"]


def memory_per_gpu(m, tp, pp, dp, zero, micro, checkpoint, accum):
    psi = params(m) / (tp * pp)
    states = 2 * psi / (dp if zero >= 3 else 1) + 2 * psi / (dp if zero >= 2 else 1) + 12 * psi / (dp if zero >= 1 else 1)
    layers = -(-m["layers"] // pp)
    in_flight = min(pp, accum)
    per_layer = SEQ * micro * m["d"] * 34 / tp
    if checkpoint:
        acts = layers * in_flight * 2 * SEQ * micro * m["d"] / tp + per_layer
    else:
        acts = layers * in_flight * per_layer
    return states + acts


# %% [markdown]
# Choose the plan: tensor-parallel degree `tp` (inside a server), pipeline stages `pp`, data-parallel
# degree `dp`, ZeRO stage, micro-batch size, and whether to checkpoint. `accum`, the micro-batches
# each data-parallel replica runs per step, follows from the global batch. Keep the memory below
# 90% of the card and the pipeline bubble below 10%.

# %%
# BEGIN SOLUTION -> PLAN = None
PLAN = dict(tp=1, pp=1, dp=64, zero=1, micro=1, checkpoint=False)
# END SOLUTION
accum = GLOBAL_SEQS // (PLAN["dp"] * PLAN["micro"])
plan_bytes = memory_per_gpu(MODEL, PLAN["tp"], PLAN["pp"], PLAN["dp"], PLAN["zero"], PLAN["micro"], PLAN["checkpoint"], accum)
bubble = (PLAN["pp"] - 1) / (accum + PLAN["pp"] - 1)
print(f"{params(MODEL) / 1e9:.1f}B parameters; {plan_bytes / 2 ** 30:.1f} GiB per GPU of {GPU_BYTES / 2 ** 30:.0f}; "
      f"{accum} micro-batches per step; bubble {bubble:.1%}")

# %% [markdown]
# ## Part 2. Four processes on one machine
#
# `run_parallel(fn, *args)` forks `WORLD` processes, joins them into a gloo process group and returns
# the value of `fn(rank, world, *args)` from each, in rank order. Collectives time out after a
# minute instead of hanging forever.

# %%
def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    return port


def _convert(value, tensor_fn):
    """Apply tensor_fn to every tensor (or array) inside nested tuples and lists."""
    if isinstance(value, (list, tuple)):
        return type(value)(_convert(v, tensor_fn) for v in value)
    return tensor_fn(value)


def _worker(fn, rank, world, port, args, queue):
    torch.set_num_threads(1)
    try:
        dist.init_process_group("gloo", rank=rank, world_size=world, init_method=f"tcp://127.0.0.1:{port}", timeout=timedelta(seconds=60))
        # Results travel by value: a tensor sent through the queue would point at this process's memory.
        out = _convert(fn(rank, world, *args), lambda v: v.detach().numpy().copy() if isinstance(v, torch.Tensor) else v)
        queue.put((rank, "ok", out))
    except Exception:
        queue.put((rank, "error", traceback.format_exc()))
    finally:
        if dist.is_initialized():
            dist.destroy_process_group()


def run_parallel(fn, *args, world=WORLD):
    ctx = mp.get_context("fork")
    queue = ctx.SimpleQueue()
    port = _free_port()
    procs = [ctx.Process(target=_worker, args=(fn, r, world, port, args, queue)) for r in range(world)]
    for p in procs:
        p.start()
    results = dict()
    for _ in procs:
        rank, status, value = queue.get()
        if status == "error":
            raise RuntimeError(f"rank {rank} failed:\n{value}")
        results[rank] = _convert(value, lambda v: torch.from_numpy(v) if hasattr(v, "__array__") and not isinstance(v, (int, float)) else v)
    for p in procs:
        p.join()
    return [results[r] for r in range(world)]


print(run_parallel(lambda rank, world: f"rank {rank} of {world}"))

# %% [markdown]
# ## 3. Ring collectives from messages
#
# Write `ring_reduce_scatter(x, rank, world)` and `ring_all_gather(chunk, rank, world)` exactly as
# in exercise 2, but with real messages: in each step, send one chunk to the right neighbour with
# `dist.isend` while receiving one from the left with `dist.recv`, then `wait()` on the send.
# After the reduce-scatter, rank `r` returns the fully summed chunk `(r + 1) % world`; the
# all-gather takes that chunk and returns the whole concatenated array.

# %%
def ring_reduce_scatter(x, rank, world):
    # BEGIN SOLUTION
    chunks = [c.clone() for c in x.chunk(world)]
    right, left = (rank + 1) % world, (rank - 1) % world
    for s in range(world - 1):
        send_i, recv_i = (rank - s) % world, (rank - s - 1) % world
        buf = torch.empty_like(chunks[recv_i])
        req = dist.isend(chunks[send_i], dst=right)
        dist.recv(buf, src=left)
        req.wait()
        chunks[recv_i] += buf
    return chunks[(rank + 1) % world]
    # END SOLUTION


def ring_all_gather(chunk, rank, world):
    # BEGIN SOLUTION
    chunks = [None] * world
    chunks[(rank + 1) % world] = chunk.clone()
    right, left = (rank + 1) % world, (rank - 1) % world
    for s in range(world - 1):
        send_i, recv_i = (rank + 1 - s) % world, (rank - s) % world
        buf = torch.empty_like(chunk)
        req = dist.isend(chunks[send_i], dst=right)
        dist.recv(buf, src=left)
        req.wait()
        chunks[recv_i] = buf
    return torch.cat(chunks)
    # END SOLUTION


def check_ring(rank, world):
    x = torch.arange(12, dtype=torch.float64) * (rank + 1) + rank
    mine = ring_all_gather(ring_reduce_scatter(x, rank, world), rank, world)
    ref = x.clone()
    dist.all_reduce(ref)
    return (mine - ref).abs().max().item()


ring_errors = run_parallel(check_ring)
print("ring all-reduce vs dist.all_reduce, largest difference per rank:", ring_errors)

# %% [markdown]
# ## 4. Data parallelism
#
# Every rank builds the same model from the same seed and trains on its quarter of the batch. Write
# `average_gradients(model, world)`: all-reduce every parameter's gradient and divide by the number
# of ranks, so that each rank applies the full-batch gradient.

# %%
STEPS = 5 if SMALL else 20


def make_model():
    torch.manual_seed(0)
    return nn.Sequential(nn.Linear(8, 32), nn.Tanh(), nn.Linear(32, 1)).double()


def make_data():
    g = torch.Generator().manual_seed(1)
    X = torch.randn(64, 8, generator=g, dtype=torch.float64)
    return X, torch.sin(X.sum(1, keepdim=True))


def average_gradients(model, world):
    # BEGIN SOLUTION
    for p in model.parameters():
        dist.all_reduce(p.grad)
        p.grad /= world
    # END SOLUTION


def ddp_worker(rank, world):
    model = make_model()
    X, y = make_data()
    Xr, yr = X.chunk(world)[rank], y.chunk(world)[rank]
    opt = torch.optim.SGD(model.parameters(), lr=0.1)
    for _ in range(STEPS):
        opt.zero_grad()
        F.mse_loss(model(Xr), yr).backward()
        average_gradients(model, world)
        opt.step()
    return torch.nn.utils.parameters_to_vector(model.parameters()).detach()


def reference_sgd():
    model = make_model()
    X, y = make_data()
    opt = torch.optim.SGD(model.parameters(), lr=0.1)
    for _ in range(STEPS):
        opt.zero_grad()
        F.mse_loss(model(X), y).backward()
        opt.step()
    return torch.nn.utils.parameters_to_vector(model.parameters()).detach()


ddp_params = run_parallel(ddp_worker)
ddp_error = max((p - reference_sgd()).abs().max().item() for p in ddp_params)
print(f"data parallel vs one process: largest difference {ddp_error:.2e}")

# %% [markdown]
# ## 5. ZeRO stage 1
#
# Now each rank keeps Adam's moments only for its own slice of the flattened parameters: the slice
# that `ring_reduce_scatter` leaves it, chunk `(rank + 1) % world`. Write `zero1_worker`: after
# backward, flatten the gradients, reduce-scatter them and divide by the number of ranks, update
# your slice with Adam (bias-corrected, `lr=0.01`, betas `(0.9, 0.999)`, `eps=1e-8`), all-gather
# the updated slices and copy them back into the model. Return the final parameter vector and the
# number of optimizer-state elements this rank stored.

# %%
def zero1_worker(rank, world, lr=0.01, b1=0.9, b2=0.999, eps=1e-8):
    model = make_model()
    X, y = make_data()
    Xr, yr = X.chunk(world)[rank], y.chunk(world)[rank]
    n = sum(p.numel() for p in model.parameters())
    pad = -n % world
    # BEGIN SOLUTION
    flat = torch.cat([torch.nn.utils.parameters_to_vector(model.parameters()).detach(), torch.zeros(pad, dtype=torch.float64)])
    own = (rank + 1) % world
    size = flat.numel() // world
    m = torch.zeros(size, dtype=torch.float64)
    v = torch.zeros(size, dtype=torch.float64)
    for t in range(1, STEPS + 1):
        model.zero_grad()
        F.mse_loss(model(Xr), yr).backward()
        g = torch.cat([torch.cat([p.grad.flatten() for p in model.parameters()]), torch.zeros(pad, dtype=torch.float64)])
        g_own = ring_reduce_scatter(g, rank, world) / world
        w_own = flat[own * size:(own + 1) * size]
        m = b1 * m + (1 - b1) * g_own
        v = b2 * v + (1 - b2) * g_own ** 2
        w_own = w_own - lr * (m / (1 - b1 ** t)) / ((v / (1 - b2 ** t)).sqrt() + eps)
        flat = ring_all_gather(w_own, rank, world)
        torch.nn.utils.vector_to_parameters(flat[:n], model.parameters())
    return flat[:n], m.numel() + v.numel()
    # END SOLUTION


def reference_adam(lr=0.01):
    model = make_model()
    X, y = make_data()
    opt = torch.optim.Adam(model.parameters(), lr=lr, betas=(0.9, 0.999), eps=1e-8)
    for _ in range(STEPS):
        opt.zero_grad()
        F.mse_loss(model(X), y).backward()
        opt.step()
    return torch.nn.utils.parameters_to_vector(model.parameters()).detach()


zero_out = run_parallel(zero1_worker)
n_params = sum(p.numel() for p in make_model().parameters())
zero_error = max((w - reference_adam()).abs().max().item() for w, _ in zero_out)
zero_state = [s for _, s in zero_out]
print(f"ZeRO-1 vs torch.optim.Adam: largest difference {zero_error:.2e}; optimizer state per rank {zero_state} "
      f"elements against {2 * n_params} unsharded")

# %% [markdown]
# ## 6. A tensor-parallel MLP
#
# Megatron-LM writes tensor parallelism with two autograd functions. `CopyToParallel` is the
# identity in forward and all-reduces the gradient in backward (every rank uses the same input, so
# the input's gradient is the sum of theirs). `ReduceFromParallel` all-reduces in forward and is the
# identity in backward. Write both, then `tp_mlp`: rank `r` holds columns `r` of the first layer
# (split into `world` blocks) and the matching rows of the second.

# %%
class CopyToParallel(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        # BEGIN SOLUTION
        return x.clone()
        # END SOLUTION

    @staticmethod
    def backward(ctx, grad):
        # BEGIN SOLUTION
        grad = grad.clone()
        dist.all_reduce(grad)
        return grad
        # END SOLUTION


class ReduceFromParallel(torch.autograd.Function):
    @staticmethod
    def forward(ctx, x):
        # BEGIN SOLUTION
        x = x.clone()
        dist.all_reduce(x)
        return x
        # END SOLUTION

    @staticmethod
    def backward(ctx, grad):
        # BEGIN SOLUTION
        return grad
        # END SOLUTION


def tp_mlp(x, W1_r, b1_r, W2_r, b2):
    h = F.gelu(CopyToParallel.apply(x) @ W1_r + b1_r)
    return ReduceFromParallel.apply(h @ W2_r) + b2


def tp_worker(rank, world):
    g = torch.Generator().manual_seed(2)
    x = torch.randn(5, 16, generator=g, dtype=torch.float64, requires_grad=True)
    W1 = torch.randn(16, 64, generator=g, dtype=torch.float64) / 4
    b1 = torch.randn(64, generator=g, dtype=torch.float64) / 4
    W2 = torch.randn(64, 16, generator=g, dtype=torch.float64) / 8
    b2 = torch.randn(16, generator=g, dtype=torch.float64)
    cols = slice(rank * 64 // world, (rank + 1) * 64 // world)
    W1_r = W1[:, cols].clone().requires_grad_()
    b1_r = b1[cols].clone().requires_grad_()
    W2_r = W2[cols, :].clone().requires_grad_()
    y = tp_mlp(x, W1_r, b1_r, W2_r, b2)
    y.pow(2).sum().backward()
    xd, W1d, W2d = x.detach().clone().requires_grad_(), W1.clone().requires_grad_(), W2.clone().requires_grad_()
    yd = F.gelu(xd @ W1d + b1) @ W2d + b2
    yd.pow(2).sum().backward()
    return max(
        (y - yd).abs().max().item(),
        (x.grad - xd.grad).abs().max().item(),
        (W1_r.grad - W1d.grad[:, cols]).abs().max().item(),
        (W2_r.grad - W2d.grad[cols, :]).abs().max().item(),
    )


tp_errors = run_parallel(tp_worker)
print("tensor-parallel MLP vs dense, largest difference per rank:", tp_errors)

# %% [markdown]
# ## 7. Activation checkpointing
#
# Count the bytes autograd saves for backward through a stack of eight blocks, with and without
# `torch.utils.checkpoint` around each block. Write `saved_bytes(fn)`, which runs `fn()` inside
# `torch.autograd.graph.saved_tensors_hooks` and adds up the size of every tensor packed.

# %%
def saved_bytes(fn):
    # BEGIN SOLUTION
    total = [0]

    def pack(t):
        total[0] += t.numel() * t.element_size()
        return t

    with torch.autograd.graph.saved_tensors_hooks(pack, lambda t: t):
        fn()
    return total[0]
    # END SOLUTION


blocks = nn.ModuleList([nn.Sequential(nn.Linear(256, 1024), nn.GELU(), nn.Linear(1024, 256)) for _ in range(8)])
inp = torch.randn(64, 256, requires_grad=True)


def run_plain():
    h = inp
    for b in blocks:
        h = h + b(h)
    return h.sum()


def run_checkpointed():
    h = inp
    for b in blocks:
        h = h + torch.utils.checkpoint.checkpoint(b, h, use_reentrant=False)
    return h.sum()


plain_bytes, ckpt_bytes = saved_bytes(run_plain), saved_bytes(run_checkpointed)
print(f"saved for backward: {plain_bytes / 2 ** 20:.2f} MiB plain, {ckpt_bytes / 2 ** 20:.2f} MiB checkpointed")

# %% [markdown]
# ## 8. Report
#
# In `REPORT`, write at least 80 words justifying your plan: the memory per GPU, why each degree of
# parallelism is what it is, the communication it implies, and what you would change for a
# 70-billion-parameter model.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
REPORT = f"""The 13B model needs {16 * params(MODEL) / 1e9:.0f} GB of model states, so plain data parallelism does not fit.
With ZeRO stage 1 over all 64 GPUs each GPU keeps 16-bit weights and gradients but only a 64th of the fp32 optimizer
states, and with micro-batches of one 2048-token sequence and FlashAttention the activations stay small, so the plan
uses {plan_bytes / 2 ** 30:.1f} GiB of 80 and needs no tensor or pipeline parallelism, no bubble and no checkpointing.
Communication is one reduce-scatter and one all-gather of the gradients per step, the same traffic as data
parallelism, overlapped with backward; each GPU sends about 2 x 26 GB per step over the network, which is the
cost to watch. For a 70B model the 16-bit weights and gradients alone take 280 GB, so I would move to ZeRO stage 3
or add 8-way tensor parallelism inside each server and use pipeline stages across servers."""
# END SOLUTION
print(REPORT)
