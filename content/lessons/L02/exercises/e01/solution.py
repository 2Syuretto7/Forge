import numpy as np


def moments(values, probs):
    """Return (mean, variance) of the discrete distribution, as floats."""
    values = np.asarray(values, dtype=float)
    probs = np.asarray(probs, dtype=float)
    m = float(np.sum(values * probs))
    v = float(np.sum((values - m) ** 2 * probs))
    return m, v


def affine_moments(mean, var, a, b):
    """Return (mean, variance) of a*X + b."""
    return a * mean + b, a * a * var


def average_variance(var, n):
    """Variance of the mean of n independent copies."""
    return var / n
