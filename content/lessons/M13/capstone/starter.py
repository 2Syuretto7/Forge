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
    raise NotImplementedError


def google_dense(n, src, dst, d=0.85):
    """Dense Google matrix."""
    raise NotImplementedError


def second_eigenvalue(G):
    """Second largest |eigenvalue|."""
    raise NotImplementedError


def predicted_steps(lam2, tol, r0):
    """Steps for r0 to fall below tol at rate |lam2|."""
    raise NotImplementedError


def top(scores, k=10):
    """Indices of the k best pages."""
    raise NotImplementedError
