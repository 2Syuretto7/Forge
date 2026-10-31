import numpy as np


def model(theta, x):
    """E + A x^(-alpha)."""
    raise NotImplementedError


def jacobian(theta, x):
    """Derivatives of the model in E, A and alpha."""
    raise NotImplementedError


def fit(x, y, theta0, iters=100):
    """Levenberg-Marquardt fit."""
    raise NotImplementedError


def param_cov(x, y, theta):
    """s^2 (J^T J)^(-1)."""
    raise NotImplementedError


def standard_errors(x, y, theta):
    """Standard errors of the fitted parameters."""
    raise NotImplementedError
