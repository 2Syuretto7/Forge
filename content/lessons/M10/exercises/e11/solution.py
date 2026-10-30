import time

import numpy as np


def time_matmul(n, repeats=3, seed=0):
    """Fastest of several timings of an n by n product."""
    rng = np.random.default_rng(seed)
    A, B = rng.normal(size=(n, n)), rng.normal(size=(n, n))
    best = float("inf")
    for _ in range(repeats):
        t0 = time.perf_counter()
        A @ B
        best = min(best, time.perf_counter() - t0)
    return best


def fit_exponent(ns, times):
    """Slope of log(time) against log(n)."""
    return float(np.polyfit(np.log(ns), np.log(times), 1)[0])


def predicted_ratio(n1, n2):
    """(n2 / n1) cubed."""
    return (n2 / n1) ** 3
