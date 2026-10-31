import numpy as np


def sign_pair(n, rng):
    """x standard normal, y = s x with an independent random sign."""
    raise NotImplementedError


def correlation(x, y):
    """Sample correlation."""
    raise NotImplementedError


def square_correlation(x, y):
    """Correlation of the squares."""
    raise NotImplementedError


def zero_sum_fraction(x, y, tol=1e-12):
    """Fraction of pairs whose sum is zero."""
    raise NotImplementedError
