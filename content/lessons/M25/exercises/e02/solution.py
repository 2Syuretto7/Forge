import numpy as np


def rate_mle(x):
    """Maximum-likelihood estimate of an exponential rate."""
    return 1.0 / np.mean(x)


def rate_unbiased(x):
    """Unbiased estimate of an exponential rate."""
    x = np.asarray(x, dtype=float)
    return (len(x) - 1) / np.sum(x)


def simulate_rate_bias(n, lam, trials, seed=0):
    """(average MLE - lam, average unbiased estimate - lam)."""
    X = np.random.default_rng(seed).exponential(1 / lam, size=(trials, n))
    s = X.sum(axis=1)
    return float(np.mean(n / s) - lam), float(np.mean((n - 1) / s) - lam)
