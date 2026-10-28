# %% [markdown]
# # L11 capstone: measure, profile and speed up a training step
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. You will
# (1) benchmark matrix products and elementwise additions and place them on the T4's roofline,
# (2) measure host-to-device copies, (3) profile a deliberately slow training step, and
# (4) write a version that is at least twice as fast and produces the same losses. The last cell is
# the autograder; it prints a completion code to paste into the lesson.

# %%
import math
import os
import time

import numpy as np
import torch

SMALL = os.environ.get("SMALL") == "1"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
torch.manual_seed(0)
print("device:", torch.cuda.get_device_name(0) if DEVICE == "cuda" else "CPU (switch the runtime to a T4 GPU for real numbers)")


def sync():
    if DEVICE == "cuda":
        torch.cuda.synchronize()


def timeit(fn, warmup=3, repeats=10):
    """Median seconds per call. GPU work is asynchronous, so synchronize before reading the clock."""
    for _ in range(warmup):
        fn()
    sync()
    ts = []
    for _ in range(repeats):
        if DEVICE == "cuda":
            start, end = torch.cuda.Event(enable_timing=True), torch.cuda.Event(enable_timing=True)
            start.record()
            fn()
            end.record()
            torch.cuda.synchronize()
            ts.append(start.elapsed_time(end) / 1e3)
        else:
            t = time.perf_counter()
            fn()
            ts.append(time.perf_counter() - t)
    return float(np.median(ts))


# %% [markdown]
# ## 1. Benchmarks on the roofline
#
# For every kernel, record its FLOPs and the minimum bytes it must move (each input read once, the
# output written once). Fill in the two counts where marked.

# %%
DTYPE = torch.float16 if DEVICE == "cuda" else torch.float32
BYTES = torch.finfo(DTYPE).bits // 8
bench = []
for n in ([128, 512] if SMALL else [256, 512, 1024, 2048, 4096]):
    a = torch.randn(n, n, device=DEVICE, dtype=DTYPE)
    b = torch.randn(n, n, device=DEVICE, dtype=DTYPE)
    t = timeit(lambda: a @ b)
    # BEGIN SOLUTION -> flops, nbytes = 0, 0  # the matmul's FLOPs and minimum bytes
    flops, nbytes = 2 * n ** 3, 3 * n * n * BYTES
    # END SOLUTION
    bench.append({"name": f"matmul {n}", "flops": flops, "bytes": nbytes, "seconds": t})
for n in ([1 << 14, 1 << 18] if SMALL else [1 << 16, 1 << 20, 1 << 24, 1 << 26]):
    x = torch.randn(n, device=DEVICE, dtype=DTYPE)
    y = torch.randn(n, device=DEVICE, dtype=DTYPE)
    t = timeit(lambda: x + y)
    # BEGIN SOLUTION -> flops, nbytes = 0, 0  # the addition's FLOPs and minimum bytes
    flops, nbytes = n, 3 * n * BYTES
    # END SOLUTION
    bench.append({"name": f"add {n}", "flops": flops, "bytes": nbytes, "seconds": t})

for r in bench:
    r["intensity"] = r["flops"] / max(r["bytes"], 1)
    r["tflops"] = r["flops"] / r["seconds"] / 1e12
    r["gbps"] = r["bytes"] / r["seconds"] / 1e9
    print(f"{r['name']:>14}: {r['intensity']:8.2f} FLOP/B  {r['tflops']:8.3f} TFLOP/s  {r['gbps']:8.1f} GB/s")

# %%
# The T4's roofs (datasheet): 65 TFLOP/s fp16 on tensor cores, 8.1 fp32, 320 GB/s of memory bandwidth.
try:
    import matplotlib.pyplot as plt

    peak = 65e12 if DTYPE == torch.float16 else 8.1e12
    xs = np.logspace(-2, 4, 200)
    plt.loglog(xs, np.minimum(peak, 320e9 * xs) / 1e12, label="T4 roofline")
    for r in bench:
        plt.loglog(r["intensity"], r["tflops"], "o")
        plt.annotate(r["name"], (r["intensity"], r["tflops"]), fontsize=8)
    plt.xlabel("arithmetic intensity (FLOP/byte)")
    plt.ylabel("TFLOP/s")
    plt.legend()
    plt.show()
except ImportError:
    print("matplotlib is not installed; skipping the plot")

# %% [markdown]
# ## 2. Host-to-device copies
#
# Copy the same buffer from ordinary (pageable) host memory and from pinned host memory.

# %%
NB = (1 << 20) if SMALL else (64 << 20)
host = torch.empty(NB, dtype=torch.uint8)
pinned = torch.empty(NB, dtype=torch.uint8, pin_memory=(DEVICE == "cuda"))
dev = torch.empty(NB, dtype=torch.uint8, device=DEVICE)
transfer = {
    "pageable_gbps": NB / timeit(lambda: dev.copy_(host)) / 1e9,
    "pinned_gbps": NB / timeit(lambda: dev.copy_(pinned, non_blocking=True)) / 1e9,
}
print(transfer)

# %% [markdown]
# ## 3. A slow training step
#
# `slow_step` trains a two-layer MLP regression on random data with plain SGD. It is correct and
# slow. Do not change it; profile it, then write `fast_step` below.

# %%
D, HID, B = (64, 256, 32) if SMALL else (1024, 4096, 256)
STEPS = 6 if SMALL else 30
LR = 0.05


def make_params(seed=0):
    g = torch.Generator().manual_seed(seed)
    W1 = torch.randn(D, HID, generator=g) / math.sqrt(D)
    W2 = torch.randn(HID, D, generator=g) / math.sqrt(HID)
    return [t.to(DEVICE).requires_grad_() for t in (W1, torch.zeros(HID), W2, torch.zeros(D))]


def batch(step):
    rng = np.random.default_rng(step)
    return rng.normal(size=(B, D)), rng.normal(size=(B, D))


def slow_gelu(x):
    inner = (x + 0.044715 * x * x * x) * math.sqrt(2.0 / math.pi)
    return 0.5 * x * (1.0 + torch.tanh(inner))


def slow_step(params, step):
    xb, yb = batch(step)
    x = torch.tensor(xb, dtype=torch.float32).to(DEVICE)
    y = torch.tensor(yb, dtype=torch.float32).to(DEVICE)
    W1, b1, W2, b2 = params
    out = slow_gelu(x @ W1 + b1) @ W2 + b2
    loss = ((out - y) ** 2).mean()
    loss.backward()
    with torch.no_grad():
        for p in params:
            p -= LR * p.grad
            p.grad = None
    return loss.item()


P = make_params()
slow_losses = [slow_step(P, s) for s in range(STEPS)]
P = make_params()
sync()
t0 = time.perf_counter()
for s in range(STEPS):
    slow_step(P, s)
sync()
slow_time = (time.perf_counter() - t0) / STEPS
print(f"slow step: {slow_time * 1e3:.2f} ms")

# %%
from torch.profiler import ProfilerActivity, profile

ACTIVITIES = [ProfilerActivity.CPU] + ([ProfilerActivity.CUDA] if DEVICE == "cuda" else [])
SORT = "cuda_time_total" if DEVICE == "cuda" else "cpu_time_total"


def kernel_count(prof, steps):
    """Device kernels per step on a GPU; on a CPU, ATen operator calls per step."""
    # BEGIN SOLUTION
    if DEVICE == "cuda":
        n = sum(1 for e in prof.events() if e.device_type == torch.autograd.DeviceType.CUDA)
    else:
        n = sum(1 for e in prof.events() if e.name.startswith("aten::"))
    return n / steps
    # END SOLUTION


P = make_params()
with profile(activities=ACTIVITIES) as prof_slow:
    for s in range(3):
        slow_step(P, s)
print(prof_slow.key_averages().table(sort_by=SORT, row_limit=12))
slow_kernels = kernel_count(prof_slow, 3)
print("per step:", slow_kernels)

# %% [markdown]
# ## 4. Your fast step
#
# Write `prepare(steps)`, which may move all the data to the device in advance, and
# `fast_step(params, opt, data, step)`, which must compute the same losses as `slow_step` for the
# same parameters and data. Return the loss as a tensor (not a Python float), so nothing forces the
# CPU to wait for the GPU. `make_optimizer(params)` may return any object you need, such as a
# `torch.optim` optimizer.

# %%
def prepare(steps):
    # BEGIN SOLUTION
    xs, ys = zip(*(batch(s) for s in range(steps)))
    x = torch.tensor(np.stack(xs), dtype=torch.float32).to(DEVICE)
    y = torch.tensor(np.stack(ys), dtype=torch.float32).to(DEVICE)
    return x, y
    # END SOLUTION


def make_optimizer(params):
    # BEGIN SOLUTION
    return torch.optim.SGD(params, lr=LR, foreach=True)
    # END SOLUTION


def fast_step(params, opt, data, step):
    # BEGIN SOLUTION
    x, y = data[0][step], data[1][step]
    W1, b1, W2, b2 = params
    with torch.autocast(device_type="cuda", dtype=torch.float16, enabled=(DEVICE == "cuda")):
        h = torch.nn.functional.gelu(torch.addmm(b1, x, W1), approximate="tanh")
        out = torch.addmm(b2, h, W2)
    loss = ((out.float() - y) ** 2).mean()
    loss.backward()
    opt.step()
    opt.zero_grad(set_to_none=True)
    return loss.detach()
    # END SOLUTION


data = prepare(STEPS)
P = make_params()
opt = make_optimizer(P)
fast_losses = [float(v) for v in [fast_step(P, opt, data, s) for s in range(STEPS)]]
P = make_params()
opt = make_optimizer(P)
for s in range(2):
    fast_step(P, opt, data, s)
sync()
t0 = time.perf_counter()
for s in range(STEPS):
    fast_step(P, opt, data, s)
sync()
fast_time = (time.perf_counter() - t0) / STEPS
speedup = slow_time / fast_time
print(f"fast step: {fast_time * 1e3:.2f} ms, speedup {speedup:.1f}x")
print("largest loss difference:", max(abs(a - b) for a, b in zip(slow_losses, fast_losses)))

P = make_params()
opt = make_optimizer(P)
with profile(activities=ACTIVITIES) as prof_fast:
    for s in range(3):
        fast_step(P, opt, data, s)
    sync()
print(prof_fast.key_averages().table(sort_by=SORT, row_limit=12))
fast_kernels = kernel_count(prof_fast, 3)
print("per step:", fast_kernels)

# %% [markdown]
# ## 5. Report
#
# In at least 80 words: what the profiler showed in the slow step (where the time went, how many
# kernels ran), each change you made and why it helps, and your measured speedup.

# %%
# BEGIN SOLUTION -> REPORT = """Write your report here."""
REPORT = """
The profiler showed that the slow step spent most of its time outside the GPU's arithmetic: every
step generated its batch with NumPy on the CPU, converted it from float64, copied it from pageable
memory, launched eight separate elementwise kernels for the GELU in the forward pass and more in the
backward pass, updated the four parameters with separate small kernels, and called .item(), which
made the CPU wait for the GPU at the end of every step. The fast step moves all batches to the device
once before training, uses the fused tanh GELU and addmm so bias, matmul and activation take fewer
kernels, runs the matrix products in fp16 under autocast on the tensor cores, updates the parameters
with a foreach SGD, and returns the loss as a tensor so the CPU keeps queueing work. The losses
agree with the slow step to within fp16 rounding, and the measured speedup is printed above.
"""
# END SOLUTION
