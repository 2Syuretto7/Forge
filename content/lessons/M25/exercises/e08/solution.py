import numpy as np


def posterior_params(a, b, k, n):
    """Return (alpha, beta) of the posterior Beta."""
    return a + k, b + n - k


def map_estimate(a, b, k, n):
    """Posterior mode."""
    al, be = posterior_params(a, b, k, n)
    return (al - 1) / (al + be - 2)


def posterior_mean(a, b, k, n):
    """Posterior mean."""
    al, be = posterior_params(a, b, k, n)
    return al / (al + be)


def credible_interval(alpha, beta, level=0.95, draws=100000, seed=0):
    """Equal-tailed interval (lo, hi) from Monte Carlo samples of Beta(alpha, beta)."""
    s = np.random.default_rng(seed).beta(alpha, beta, size=draws)
    lo, hi = np.quantile(s, [(1 - level) / 2, (1 + level) / 2])
    return float(lo), float(hi)
