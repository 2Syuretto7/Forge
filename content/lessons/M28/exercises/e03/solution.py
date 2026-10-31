import numpy as np


def jensen_gap(f, samples, weights=None):
    """E f(X) - f(E X) under the empirical (or weighted) distribution."""
    x = np.asarray(samples, dtype=float)
    w = np.full(len(x), 1 / len(x)) if weights is None else np.asarray(weights, dtype=float)
    return float(np.sum(w * f(x)) - f(np.sum(w * x)))


def am_gm(x):
    """(arithmetic mean, geometric mean)."""
    x = np.asarray(x, dtype=float)
    return float(x.mean()), float(np.exp(np.mean(np.log(x))))


def log_mean_exp(x):
    """log of the mean of exp(x), stably."""
    x = np.asarray(x, dtype=float)
    m = x.max()
    return float(m + np.log(np.mean(np.exp(x - m))))
