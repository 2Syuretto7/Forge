import numpy as np


def sample_exponential(n, rate, seed=0):
    """Exponential by inverse CDF."""
    raise NotImplementedError


def sample_cauchy(n, seed=0):
    """Cauchy by inverse CDF."""
    raise NotImplementedError


def sample_from_table(xs, cdf_values, n, seed=0):
    """Inverse CDF by interpolation in a table."""
    raise NotImplementedError
