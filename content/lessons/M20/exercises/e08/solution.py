import numpy as np


def sample_exponential(n, rate, seed=0):
    """Exponential by inverse CDF."""
    return -np.log(1 - np.random.default_rng(seed).random(n)) / rate


def sample_cauchy(n, seed=0):
    """Cauchy by inverse CDF."""
    return np.tan(np.pi * (np.random.default_rng(seed).random(n) - 0.5))


def sample_from_table(xs, cdf_values, n, seed=0):
    """Inverse CDF by interpolation in a table."""
    return np.interp(np.random.default_rng(seed).random(n), cdf_values, xs)
