import numpy as np


def jensen_gap(f, samples, weights=None):
    """E f(X) - f(E X) under the empirical (or weighted) distribution."""
    raise NotImplementedError


def am_gm(x):
    """(arithmetic mean, geometric mean)."""
    raise NotImplementedError


def log_mean_exp(x):
    """log of the mean of exp(x), stably."""
    raise NotImplementedError
