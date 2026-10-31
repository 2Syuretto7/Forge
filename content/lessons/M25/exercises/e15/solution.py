import math
import numpy as np


# provided
def ar1(n, rho, rng):
    e = rng.standard_normal(n)
    x = np.empty(n)
    x[0] = e[0]
    s = math.sqrt(1 - rho * rho)
    for t in range(1, n):
        x[t] = rho * x[t - 1] + s * e[t]
    return x


def iid_bootstrap_se(x, B, rng):
    """Bootstrap standard error of the mean, resampling single points."""
    x = np.asarray(x, dtype=float)
    return float(x[rng.integers(0, len(x), size=(B, len(x)))].mean(axis=1).std())


def block_bootstrap_se(x, block, B, rng):
    """Bootstrap standard error of the mean, resampling blocks."""
    x = np.asarray(x, dtype=float)
    n = len(x)
    starts = rng.integers(0, n - block + 1, size=(B, n // block))
    return float(x[starts[..., None] + np.arange(block)].mean(axis=(1, 2)).std())
