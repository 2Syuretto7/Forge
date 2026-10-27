import numpy as np


def posterior_params(a, b, k, n):
    """Return (alpha, beta) of the posterior Beta."""
    raise NotImplementedError


def map_estimate(a, b, k, n):
    """Posterior mode."""
    raise NotImplementedError


def posterior_mean(a, b, k, n):
    """Posterior mean."""
    raise NotImplementedError


def credible_interval(alpha, beta, level=0.95, draws=100000, seed=0):
    """Equal-tailed interval (lo, hi) from Monte Carlo samples of Beta(alpha, beta)."""
    raise NotImplementedError
