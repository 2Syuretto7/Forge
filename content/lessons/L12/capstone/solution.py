# %% [markdown]
# # L12 capstone: Triton kernels, up to FlashAttention
#
# Choose **Runtime, Change runtime type, T4 GPU**, then run the cells in order. You will write four
# Triton kernels: a fused row softmax, a tiled matrix multiplication, a fused layer norm, and the
# forward pass of FlashAttention, which must match a reference within 1e-2 in fp16 and beat the
# unfused attention at sequence length 2048. The last cell is the autograder.
#
# Without a GPU the kernels still run, slowly, in Triton's interpreter (`TRITON_INTERPRET=1`, set
# below), which is useful for debugging; the speed test needs the GPU.

# %%
import math
import os

if not os.environ.get("TRITON_INTERPRET"):
    import torch as _t
    if not _t.cuda.is_available():
        os.environ["TRITON_INTERPRET"] = "1"  # must be set before triton is imported

import torch
import triton
import triton.language as tl

SMALL = os.environ.get("SMALL") == "1"
INTERPRET = os.environ.get("TRITON_INTERPRET") == "1"
DEVICE = "cuda" if torch.cuda.is_available() and not INTERPRET else "cpu"
torch.manual_seed(0)
print("triton", triton.__version__, "| device:", DEVICE, "| interpreter" if INTERPRET else "")

# %% [markdown]
# ## 0. A first kernel: vector addition
#
# One program instance handles `BLOCK` consecutive elements. `tl.arange` gives the offsets within the
# block, a mask guards the ragged end, and loads and stores move whole blocks at once.

# %%
@triton.jit
def add_kernel(x_ptr, y_ptr, out_ptr, n, BLOCK: tl.constexpr):
    pid = tl.program_id(0)
    offs = pid * BLOCK + tl.arange(0, BLOCK)
    mask = offs < n
    tl.store(out_ptr + offs, tl.load(x_ptr + offs, mask=mask) + tl.load(y_ptr + offs, mask=mask), mask=mask)


def add(x, y):
    out = torch.empty_like(x)
    add_kernel[(triton.cdiv(x.numel(), 1024),)](x, y, out, x.numel(), BLOCK=1024)
    return out


x = torch.randn(5000, device=DEVICE)
print("add matches:", torch.allclose(add(x, x), 2 * x))

# %% [markdown]
# ## 1. A fused row softmax
#
# One program per row: load the row once, subtract its maximum, exponentiate in fp32, normalize and
# store, so the row makes one trip through device memory instead of several.

# %%
@triton.jit
def softmax_kernel(out_ptr, in_ptr, n_cols, BLOCK: tl.constexpr):
    row = tl.program_id(0)
    offs = tl.arange(0, BLOCK)
    mask = offs < n_cols
    # BEGIN SOLUTION
    x = tl.load(in_ptr + row * n_cols + offs, mask=mask, other=float("-inf")).to(tl.float32)
    e = tl.exp(x - tl.max(x, axis=0))
    y = e / tl.sum(e, axis=0)
    tl.store(out_ptr + row * n_cols + offs, y.to(out_ptr.dtype.element_ty), mask=mask)
    # END SOLUTION


def softmax(x):
    rows, cols = x.shape
    out = torch.empty_like(x)
    softmax_kernel[(rows,)](out, x.contiguous(), cols, BLOCK=triton.next_power_of_2(cols))
    return out


# %% [markdown]
# ## 2. A tiled matrix multiplication
#
# Each program computes a `BM x BN` tile of `C`, looping over `K` in steps of `BK` and accumulating
# `tl.dot` of a tile of `A` and a tile of `B` in fp32. Mask the loads so that sizes need not be
# multiples of the tile sizes.

# %%
@triton.jit
def matmul_kernel(a_ptr, b_ptr, c_ptr, M, N, K, BM: tl.constexpr, BN: tl.constexpr, BK: tl.constexpr):
    pid_m = tl.program_id(0)
    pid_n = tl.program_id(1)
    rm = pid_m * BM + tl.arange(0, BM)
    rn = pid_n * BN + tl.arange(0, BN)
    rk = tl.arange(0, BK)
    # BEGIN SOLUTION
    acc = tl.zeros([BM, BN], dtype=tl.float32)
    for k0 in range(0, K, BK):
        kk = k0 + rk
        a = tl.load(a_ptr + rm[:, None] * K + kk[None, :], mask=(rm[:, None] < M) & (kk[None, :] < K), other=0.0)
        b = tl.load(b_ptr + kk[:, None] * N + rn[None, :], mask=(kk[:, None] < K) & (rn[None, :] < N), other=0.0)
        acc += tl.dot(a, b)
    tl.store(c_ptr + rm[:, None] * N + rn[None, :], acc.to(c_ptr.dtype.element_ty), mask=(rm[:, None] < M) & (rn[None, :] < N))
    # END SOLUTION


def matmul(a, b, BM=32, BN=32, BK=32):
    M, K = a.shape
    N = b.shape[1]
    c = torch.empty(M, N, device=a.device, dtype=a.dtype)
    matmul_kernel[(triton.cdiv(M, BM), triton.cdiv(N, BN))](a.contiguous(), b.contiguous(), c, M, N, K, BM=BM, BN=BN, BK=BK)
    return c


# %% [markdown]
# ## 3. A fused layer norm
#
# One program per row: mean, variance, normalization, scale and shift in a single pass over the row
# (L10's forward pass as one kernel). Compute the statistics in fp32.

# %%
@triton.jit
def layernorm_kernel(x_ptr, w_ptr, b_ptr, y_ptr, n_cols, eps, BLOCK: tl.constexpr):
    row = tl.program_id(0)
    offs = tl.arange(0, BLOCK)
    mask = offs < n_cols
    # BEGIN SOLUTION
    x = tl.load(x_ptr + row * n_cols + offs, mask=mask, other=0.0).to(tl.float32)
    mean = tl.sum(x, axis=0) / n_cols
    xc = tl.where(mask, x - mean, 0.0)
    rstd = 1.0 / tl.sqrt(tl.sum(xc * xc, axis=0) / n_cols + eps)
    w = tl.load(w_ptr + offs, mask=mask, other=0.0).to(tl.float32)
    b = tl.load(b_ptr + offs, mask=mask, other=0.0).to(tl.float32)
    tl.store(y_ptr + row * n_cols + offs, (xc * rstd * w + b).to(y_ptr.dtype.element_ty), mask=mask)
    # END SOLUTION


def layernorm(x, w, b, eps=1e-5):
    rows, cols = x.shape
    y = torch.empty_like(x)
    layernorm_kernel[(rows,)](x.contiguous(), w, b, y, cols, eps, BLOCK=triton.next_power_of_2(cols))
    return y


# %% [markdown]
# ## 4. FlashAttention, forward pass
#
# `q`, `k`, `v` have shape `(batch * heads, N, D)`. Each program handles `BLOCK_M` queries of one
# head: it keeps a running maximum `m_i`, running sum `l_i` and an fp32 accumulator, loops over the
# keys and values in blocks of `BLOCK_N`, and rescales its running results whenever the maximum
# grows (the online softmax of the derivation). The `N x N` score matrix is never written to memory.

# %%
@triton.jit
def flash_kernel(q_ptr, k_ptr, v_ptr, o_ptr, N, scale, D: tl.constexpr, BLOCK_M: tl.constexpr, BLOCK_N: tl.constexpr):
    pid_m = tl.program_id(0)
    bh = tl.program_id(1)
    offs_m = pid_m * BLOCK_M + tl.arange(0, BLOCK_M)
    offs_d = tl.arange(0, D)
    base = bh * N * D
    q = tl.load(q_ptr + base + offs_m[:, None] * D + offs_d[None, :], mask=offs_m[:, None] < N, other=0.0)
    # BEGIN SOLUTION
    m_i = tl.full([BLOCK_M], float("-inf"), dtype=tl.float32)
    l_i = tl.zeros([BLOCK_M], dtype=tl.float32)
    acc = tl.zeros([BLOCK_M, D], dtype=tl.float32)
    for start in range(0, N, BLOCK_N):
        offs_n = start + tl.arange(0, BLOCK_N)
        kv_mask = offs_n[:, None] < N
        k = tl.load(k_ptr + base + offs_n[:, None] * D + offs_d[None, :], mask=kv_mask, other=0.0)
        v = tl.load(v_ptr + base + offs_n[:, None] * D + offs_d[None, :], mask=kv_mask, other=0.0)
        s = tl.dot(q, tl.trans(k)) * scale
        s = tl.where(offs_n[None, :] < N, s, float("-inf"))
        m_new = tl.maximum(m_i, tl.max(s, axis=1))
        p = tl.exp(s - m_new[:, None])
        alpha = tl.exp(m_i - m_new)
        l_i = l_i * alpha + tl.sum(p, axis=1)
        acc = acc * alpha[:, None] + tl.dot(p.to(v.dtype), v)
        m_i = m_new
    out = acc / l_i[:, None]
    tl.store(o_ptr + base + offs_m[:, None] * D + offs_d[None, :], out.to(o_ptr.dtype.element_ty), mask=offs_m[:, None] < N)
    # END SOLUTION


def flash_attention(q, k, v, BLOCK_M=64, BLOCK_N=64):
    BH, N, D = q.shape
    BLOCK_M, BLOCK_N = min(BLOCK_M, triton.next_power_of_2(N)), min(BLOCK_N, triton.next_power_of_2(N))
    o = torch.empty_like(q)
    grid = (triton.cdiv(N, BLOCK_M), BH)
    flash_kernel[grid](q.contiguous(), k.contiguous(), v.contiguous(), o, N, 1.0 / math.sqrt(D), D=D, BLOCK_M=BLOCK_M, BLOCK_N=BLOCK_N)
    return o


def naive_attention(q, k, v):
    """Unfused attention: the N x N score matrix is written to memory and read back."""
    s = (q @ k.transpose(1, 2)) / math.sqrt(q.shape[-1])
    return torch.softmax(s.float(), dim=-1).to(q.dtype) @ v


# %% [markdown]
# ## 5. Check and time
#
# On a T4, compare your FlashAttention with the unfused version at sequence length 2048 (16 heads of
# dimension 64, fp16). `triton.testing.do_bench` reports milliseconds per call.

# %%
DT = torch.float16
BH, N_CHECK, D = (2, 64, 16) if (SMALL or INTERPRET) else (4, 1024, 64)
q, k, v = (torch.randn(BH, N_CHECK, D, device=DEVICE, dtype=DT) for _ in range(3))
flash_error = (flash_attention(q, k, v).float() - naive_attention(q.float(), k.float(), v.float())).abs().max().item()
print(f"max |flash - reference| = {flash_error:.2e}")

timing = None
if DEVICE == "cuda" and not SMALL:
    q, k, v = (torch.randn(16, 2048, 64, device=DEVICE, dtype=DT) for _ in range(3))
    t_flash = triton.testing.do_bench(lambda: flash_attention(q, k, v))
    t_naive = triton.testing.do_bench(lambda: naive_attention(q, k, v))
    timing = {"flash_ms": t_flash, "naive_ms": t_naive}
    print(timing, f"speedup {t_naive / t_flash:.2f}x")
