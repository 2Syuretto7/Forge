import time

import numpy as np


def time_matmul(n, min_time=0.02):
    """Seconds per n x n matrix product, timing batches that double until min_time."""
    rng = np.random.default_rng(0)
    A = rng.normal(size=(n, n))
    B = rng.normal(size=(n, n))
    reps = 1
    while True:
        t0 = time.perf_counter()
        for _ in range(reps):
            A @ B
        elapsed = time.perf_counter() - t0
        if elapsed >= min_time:
            return elapsed / reps
        reps *= 2


def flops_per_second(n):
    """Measured FLOP/s of an n x n matrix product."""
    return 2 * n ** 3 / time_matmul(n)


def predict_seconds(n, rate):
    """Predicted seconds for an n x n product at rate FLOP/s."""
    return 2 * n ** 3 / rate
