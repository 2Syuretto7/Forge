import numpy as np


def lognormal_mean_factor(sigma):
    """Mean over median of a lognormal variable."""
    raise NotImplementedError


def naive_mean_prediction(A, alpha, x):
    """Exponentiated log-space fit: a median, not a mean."""
    raise NotImplementedError


def smearing_factor(residuals):
    """Duan's smearing correction."""
    raise NotImplementedError


def log_residuals(x, y, A, alpha):
    """Residuals of the log-space fit."""
    raise NotImplementedError
