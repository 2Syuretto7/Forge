import numpy as np


def fuse(m1, v1, m2, v2):
    """Product of two Gaussian densities, renormalized: (mean, variance)."""
    v = 1 / (1 / v1 + 1 / v2)
    return v * (m1 / v1 + m2 / v2), v


def fuse_many(means, variances):
    """Fuse a list of independent Gaussian measurements."""
    prec = 1 / np.asarray(variances, dtype=float)
    v = 1 / prec.sum()
    return float(v * np.sum(prec * np.asarray(means, dtype=float))), float(v)


def gain(prior_var, meas_var):
    """Kalman gain."""
    return prior_var / (prior_var + meas_var)
