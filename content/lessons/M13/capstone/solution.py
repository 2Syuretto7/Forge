import math

import numpy as np


# provided
def make_web(seed=0):
    rng = np.random.default_rng(seed)
    src, dst = [], []
    for c in range(3):
        base = 100 * c
        for i in range(100):
            page = base + i
            if c == 2 and i % 10 == 0:
                continue
            k = int(rng.integers(2, 8))
            targets = base + np.floor(100 * rng.uniform(size=k) ** 2).astype(int)
            if c == 2:
                targets = np.where(rng.uniform(size=k) < 0.5, targets - 100 * int(rng.integers(1, 3)), targets)
            for t in targets:
                if t != page:
                    src.append(page)
                    dst.append(int(t))
    return 300, np.array(src), np.array(dst)


def pagerank(n, src, dst, d=0.85, tol=1e-10, start=None):
    """(scores, steps, residuals) by sparse power iteration."""
    outdeg = np.bincount(src, minlength=n).astype(float)
    x = np.full(n, 1.0 / n) if start is None else np.asarray(start, dtype=float)
    res = []
    while True:
        follow = np.bincount(dst, weights=x[src] / outdeg[src], minlength=n)
        y = d * follow + (d * x[outdeg == 0].sum() + 1 - d) / n
        res.append(float(np.abs(y - x).sum()))
        x = y
        if res[-1] < tol:
            return x, len(res), res


def google_dense(n, src, dst, d=0.85):
    """Dense Google matrix."""
    outdeg = np.bincount(src, minlength=n).astype(float)
    S = np.zeros((n, n))
    np.add.at(S, (dst, src), 1 / outdeg[src])
    S[:, outdeg == 0] = 1 / n
    return d * S + (1 - d) / n


def second_eigenvalue(G):
    """Second largest |eigenvalue|."""
    return float(np.sort(np.abs(np.linalg.eigvals(G)))[-2])


def predicted_steps(lam2, tol, r0):
    """Steps for r0 to fall below tol at rate |lam2|."""
    return int(math.ceil(math.log(tol / r0) / math.log(abs(lam2))))


def top(scores, k=10):
    """Indices of the k best pages."""
    return [int(i) for i in np.argsort(-scores, kind="stable")[:k]]
