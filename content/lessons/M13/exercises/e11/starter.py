import math

import numpy as np


# provided
def make_graph(n, k=10, seed=0):
    rng = np.random.default_rng(seed)
    pages = np.array([i for i in range(n) if i % 20 != 0])
    src = np.repeat(pages, k)
    dst = np.floor(n * rng.uniform(size=src.size) ** 3).astype(np.int64)
    return src, dst


# provided
def pagerank_sparse(src, dst, n, d=0.85, tol=1e-10, max_iter=1000):
    outdeg = np.bincount(src, minlength=n).astype(float)
    x = np.full(n, 1.0 / n)
    res = []
    for _ in range(max_iter):
        follow = np.bincount(dst, weights=x[src] / np.maximum(outdeg[src], 1), minlength=n)
        y = d * follow + (d * x[outdeg == 0].sum() + 1 - d) / n
        res.append(float(np.abs(y - x).sum()))
        x = y
        if res[-1] < tol:
            break
    return x, res


def observed_rate(residuals):
    """Median ratio of successive residuals over the second half."""
    raise NotImplementedError


def predicted_steps(rate, tol, r0):
    """Steps for r0 to fall below tol at the given rate."""
    raise NotImplementedError
