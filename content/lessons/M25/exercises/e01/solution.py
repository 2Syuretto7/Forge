import numpy as np


def variance_estimators(x):
    """Return (biased, unbiased) variance estimates of a 1-D sample."""
    x = np.asarray(x, dtype=float)
    return float(np.var(x, ddof=0)), float(np.var(x, ddof=1))


def simulate_bias(n, sigma, trials, seed=0):
    """Return (average biased estimate - sigma^2, average unbiased estimate - sigma^2)."""
    X = np.random.default_rng(seed).normal(0, sigma, size=(trials, n))
    b = np.var(X, axis=1, ddof=0).mean() - sigma ** 2
    u = np.var(X, axis=1, ddof=1).mean() - sigma ** 2
    return float(b), float(u)
