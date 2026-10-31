import math
import numpy as np


def running_mean(x):
    """Averages of the first 1, 2, ..., n entries."""
    x = np.asarray(x, dtype=float)
    return np.cumsum(x) / np.arange(1, len(x) + 1)


def fraction_far(samples, mu, eps):
    """Fraction of rows whose mean misses mu by more than eps."""
    return float(np.mean(np.abs(np.asarray(samples, dtype=float).mean(axis=1) - mu) > eps))


def chebyshev_n(var, eps, delta):
    """Samples Chebyshev needs for P(|mean - mu| >= eps) <= delta."""
    return math.ceil(round(var / (eps**2 * delta), 9))
