import numpy as np


def gibbs(beta, K):
    """p_k proportional to exp(-beta k) on 0..K."""
    z = -beta * np.arange(K + 1)
    e = np.exp(z - z.max())
    return e / e.sum()


def mean_of(p):
    """Mean of a distribution on 0..K."""
    p = np.asarray(p, dtype=float)
    return float(np.arange(len(p)) @ p)


def max_entropy(m, K):
    """Maximum-entropy distribution on 0..K with mean m."""
    lo, hi = -50.0, 50.0
    for _ in range(200):
        mid = 0.5 * (lo + hi)
        if mean_of(gibbs(mid, K)) > m:
            lo = mid
        else:
            hi = mid
    return gibbs(0.5 * (lo + hi), K)


def entropy(p):
    """Entropy in nats."""
    p = np.asarray(p, dtype=float)
    q = p[p > 0]
    return float(-np.sum(q * np.log(q)))
