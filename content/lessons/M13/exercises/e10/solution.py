import numpy as np


def make_graph(n, k=10, seed=0):
    """(src, dst) of a random graph with popular low-numbered pages."""
    rng = np.random.default_rng(seed)
    pages = np.array([i for i in range(n) if i % 20 != 0])
    src = np.repeat(pages, k)
    dst = np.floor(n * rng.uniform(size=src.size) ** 3).astype(np.int64)
    return src, dst


def step(src, dst, outdeg, x, d):
    """x -> G x without forming G."""
    n = x.size
    follow = np.bincount(dst, weights=x[src] / outdeg[src], minlength=n)
    dangling = x[outdeg == 0].sum()
    return d * follow + (d * dangling + 1 - d) / n


def pagerank_sparse(src, dst, n, d=0.85, tol=1e-10, max_iter=1000):
    """(PageRank vector, residual per step)."""
    outdeg = np.bincount(src, minlength=n).astype(float)
    x = np.full(n, 1.0 / n)
    res = []
    for _ in range(max_iter):
        y = step(src, dst, outdeg, x, d)
        res.append(float(np.abs(y - x).sum()))
        x = y
        if res[-1] < tol:
            break
    return x, res
