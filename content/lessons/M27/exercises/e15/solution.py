import numpy as np


def kl(p, q):
    """KL(p || q) in nats."""
    p, q = np.asarray(p, dtype=float), np.asarray(q, dtype=float)
    m = p > 0
    if np.any(q[m] == 0):
        return float("inf")
    return float(np.sum(p[m] * np.log(p[m] / q[m])))


def fit(samples, K, alpha=0.0):
    """Add-alpha estimate of a categorical distribution."""
    c = np.bincount(np.asarray(samples), minlength=K).astype(float)
    return (c + alpha) / (c.sum() + K * alpha)


def heldout_ce(q, test):
    """Average negative log-probability of the test samples."""
    v = np.asarray(q, dtype=float)[np.asarray(test)]
    if np.any(v == 0):
        return float("inf")
    return float(-np.mean(np.log(v)))


def best_alpha(train, test, K, alphas):
    """The alpha with the lowest held-out cross-entropy."""
    return min(alphas, key=lambda a: heldout_ce(fit(train, K, a), test))
