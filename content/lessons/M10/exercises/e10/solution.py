import time

import numpy as np


def batched_loop(A, B):
    """Pair by pair in a Python loop."""
    return np.stack([A[i] @ B[i] for i in range(len(A))])


def batched(A, B):
    """One batched call."""
    return A @ B


def measure(b, n, seed=0):
    """(flops, seconds, flops per second) for a batch of b products of size n."""
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((b, n, n), dtype=np.float32)
    B = rng.standard_normal((b, n, n), dtype=np.float32)
    t0 = time.perf_counter()
    batched(A, B)
    dt = time.perf_counter() - t0
    flops = 2 * b * n ** 3
    return flops, dt, flops / dt
