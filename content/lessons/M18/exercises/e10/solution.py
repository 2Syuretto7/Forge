import time

import numpy as np


def f(x):
    """Softplus sum plus a smoothness penalty."""
    return float(np.sum(np.logaddexp(0.0, x)) + 0.5 * np.sum(np.diff(x) ** 2))


def grad(x):
    """Analytic gradient in O(n)."""
    d = np.diff(x)
    return 1 / (1 + np.exp(-x)) + np.concatenate([[0.0], d]) - np.concatenate([d, [0.0]])


def fd_grad(x, h=1e-6):
    """Central differences, 2n evaluations."""
    x = np.array(x, dtype=float)
    g = np.zeros_like(x)
    for i in range(x.size):
        old = x[i]
        x[i] = old + h
        fp = f(x)
        x[i] = old - h
        fm = f(x)
        x[i] = old
        g[i] = (fp - fm) / (2 * h)
    return g


def speedup(n):
    """Time of fd_grad over time of grad."""
    x = np.random.default_rng(0).normal(size=n)
    t0 = time.perf_counter()
    fd_grad(x)
    t1 = time.perf_counter()
    for _ in range(10):
        grad(x)
    t2 = time.perf_counter()
    return (t1 - t0) / ((t2 - t1) / 10)
