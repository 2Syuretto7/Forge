import numpy as np


def fit_loglog(x, y):
    """(A, alpha) from least squares on the logarithms."""
    raise NotImplementedError


def _model(theta, x):
    raise NotImplementedError


def fit_with_floor(x, y, theta0, iters=100):
    """Levenberg-Marquardt fit of E + A x^(-alpha)."""
    raise NotImplementedError


def extrapolation_errors(x, y, x0, truth):
    """Relative errors of the log-log line and the floor fit at x0."""
    raise NotImplementedError
