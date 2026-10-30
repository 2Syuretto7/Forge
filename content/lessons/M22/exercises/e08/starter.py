import numpy as np


def binomial_by_sum(n, p, size, rng):
    """Binomial(n, p) samples as sums of Bernoulli trials."""
    raise NotImplementedError


def poisson_by_arrivals(lam, size, rng):
    """Poisson(lam) samples by counting Exponential(1) arrivals before time lam."""
    raise NotImplementedError


def moments(x):
    """(sample mean, sample variance with ddof=1)."""
    raise NotImplementedError
