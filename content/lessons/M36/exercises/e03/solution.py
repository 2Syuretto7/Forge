import numpy as np


def _softmax(z):
    e = np.exp(z - np.max(z))
    return e / e.sum()


def estimates(z, r, n, rng, b=0.0):
    """Single-sample REINFORCE estimates with a constant baseline."""
    p = _softmax(z)
    a = rng.choice(len(z), size=n, p=p)
    E = np.zeros((n, len(z)))
    E[np.arange(n), a] = 1
    return (np.asarray(r)[a] - b)[:, None] * (E - p)


def total_variance(G):
    """Sum of per-component sample variances."""
    return float(np.sum(np.var(G, axis=0)))


def optimal_baseline(z, r):
    """Constant baseline minimizing the total variance."""
    p = _softmax(z)
    w = 1 - 2 * p + p @ p
    return float(np.sum(p * w * np.asarray(r)) / np.sum(p * w))
