import numpy as np


def moments(values, probs):
    """Return (mean, variance) of the discrete distribution, as floats."""
    raise NotImplementedError


def affine_moments(mean, var, a, b):
    """Return (mean, variance) of a*X + b."""
    raise NotImplementedError


def average_variance(var, n):
    """Variance of the mean of n independent copies."""
    raise NotImplementedError
