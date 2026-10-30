import numpy as np


def rope_batch(X, positions, base=10000):
    """Rotary encoding of each row of X at its position."""
    n, d = X.shape
    freqs = base ** (-np.arange(0, d, 2) / d)
    ang = np.asarray(positions, dtype=np.float64)[:, None] * freqs[None, :]
    c, s = np.cos(ang), np.sin(ang)
    a, b = X[:, 0::2], X[:, 1::2]
    out = np.empty_like(X, dtype=np.float64)
    out[:, 0::2] = a * c - b * s
    out[:, 1::2] = a * s + b * c
    return out


def relative_check(d, pairs, seed=0):
    """Largest |score(m, n) - score(m + s, n + s)| over random pairs and shifts."""
    rng = np.random.default_rng(seed)
    q, k = rng.normal(size=d), rng.normal(size=d)
    m = rng.integers(0, 2048, size=pairs)
    nn = rng.integers(0, 2048, size=pairs)
    s = rng.integers(-1000, 1000, size=pairs)
    Q = np.tile(q, (pairs, 1))
    K = np.tile(k, (pairs, 1))
    a = np.sum(rope_batch(Q, m) * rope_batch(K, nn), axis=1)
    b = np.sum(rope_batch(Q, m + s) * rope_batch(K, nn + s), axis=1)
    return float(np.max(np.abs(a - b)))
