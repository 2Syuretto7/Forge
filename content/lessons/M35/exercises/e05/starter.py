import numpy as np


def model(theta, x):
    """E + A x^(-alpha)."""
    raise NotImplementedError


def jacobian(theta, x):
    """Derivatives of the model in E, A and alpha."""
    raise NotImplementedError


def sse(theta, x, y):
    """Sum of squared residuals, infinite when not finite."""
    raise NotImplementedError


def levenberg_marquardt(x, y, theta0, lam=1e-2, iters=200):
    """Damped Gauss-Newton with an adaptive damping parameter."""
    raise NotImplementedError


def gauss_newton(x, y, theta0, iters=50):
    """Undamped Gauss-Newton, stopping at the first non-finite value."""
    raise NotImplementedError
