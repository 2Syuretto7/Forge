import time

import numpy as np


def make_database(n, d, seed=0):
    """n random float32 vectors of length d."""
    return np.random.default_rng(seed).normal(size=(n, d)).astype(np.float32)


def _normalized(X):
    return X / np.linalg.norm(X, axis=1, keepdims=True)


def search_loop(query, X, k):
    """Top-k cosine indices with a Python loop over rows."""
    U = _normalized(X)
    q = query / np.linalg.norm(query)
    scores = [float(U[i] @ q) for i in range(len(U))]
    return sorted(range(len(scores)), key=lambda i: -scores[i])[:k]


def search_vectorized(query, X, k):
    """Top-k cosine indices with one matrix-vector product."""
    U = _normalized(X)
    s = U @ (query / np.linalg.norm(query))
    idx = np.argpartition(-s, k)[:k]
    return [int(i) for i in idx[np.argsort(-s[idx])]]


def speedup(n, d, k=5):
    """Time of the loop search over time of the vectorized search."""
    X = make_database(n, d)
    q = make_database(1, d, seed=1)[0]
    t0 = time.perf_counter()
    search_loop(q, X, k)
    slow = time.perf_counter() - t0
    reps, t0 = 0, time.perf_counter()
    while time.perf_counter() - t0 < 0.02:
        search_vectorized(q, X, k)
        reps += 1
    fast = (time.perf_counter() - t0) / reps
    return slow / fast
