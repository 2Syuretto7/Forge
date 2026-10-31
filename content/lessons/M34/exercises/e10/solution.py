import math
import numpy as np


def sample_pairs(n, m, rng):
    """m random pairs of distinct indices."""
    i = rng.integers(0, n, m)
    j = (i + rng.integers(1, n, m)) % n
    return i, j


def pair_distortions(X, pairs, k, rng):
    """Relative change of squared distances under a Gaussian projection."""
    i, j = pairs
    D = X[i] - X[j]
    R = rng.standard_normal((X.shape[1], k)) / math.sqrt(k)
    return np.sum((D @ R) ** 2, axis=1) / np.sum(D * D, axis=1) - 1


def distortion_table(X, ks, m, rng):
    """Standard deviation and 99th percentile of absolute distortion for each k."""
    pairs = sample_pairs(len(X), m, rng)
    out = {}
    for k in ks:
        d = pair_distortions(X, pairs, k, rng)
        out[k] = (float(np.std(d)), float(np.quantile(np.abs(d), 0.99)))
    return out
