import numpy as np


def fuse(m1, v1, m2, v2):
    """Product of two Gaussian densities, renormalized: (mean, variance)."""
    raise NotImplementedError


def fuse_many(means, variances):
    """Fuse a list of independent Gaussian measurements."""
    raise NotImplementedError


def gain(prior_var, meas_var):
    """Kalman gain."""
    raise NotImplementedError
