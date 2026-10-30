import numpy as np


def binomial_by_sum(n, p, size, rng):
    """Binomial(n, p) samples as sums of Bernoulli trials."""
    return (rng.random((size, n)) < p).sum(axis=1)


def poisson_by_arrivals(lam, size, rng):
    """Poisson(lam) samples by counting Exponential(1) arrivals before time lam."""
    t = -np.log1p(-rng.random(size))
    k = np.zeros(size, dtype=int)
    while True:
        alive = t < lam
        if not alive.any():
            return k
        k += alive
        t = t + np.where(alive, -np.log1p(-rng.random(size)), 0.0)


def moments(x):
    """(sample mean, sample variance with ddof=1)."""
    x = np.asarray(x, dtype=float)
    return float(x.mean()), float(x.var(ddof=1))
