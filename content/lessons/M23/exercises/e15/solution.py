import numpy as np


def sign_pair(n, rng):
    """x standard normal, y = s x with an independent random sign."""
    x = rng.standard_normal(n)
    s = np.where(rng.random(n) < 0.5, -1.0, 1.0)
    return x, s * x


def correlation(x, y):
    """Sample correlation."""
    return float(np.corrcoef(x, y)[0, 1])


def square_correlation(x, y):
    """Correlation of the squares."""
    return correlation(np.asarray(x) ** 2, np.asarray(y) ** 2)


def zero_sum_fraction(x, y, tol=1e-12):
    """Fraction of pairs whose sum is zero."""
    return float(np.mean(np.abs(np.asarray(x) + np.asarray(y)) <= tol))
