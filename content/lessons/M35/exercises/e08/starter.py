import numpy as np


def prediction(theta, x0):
    """E + A x0^(-alpha)."""
    raise NotImplementedError


def grad_prediction(theta, x0):
    """Gradient of the prediction in (E, A, alpha)."""
    raise NotImplementedError


def prediction_se(theta, cov, x0):
    """Delta-method standard error of the prediction."""
    raise NotImplementedError


def band(theta, cov, xs, z=1.96):
    """Pointwise band of half-width z standard errors."""
    raise NotImplementedError
