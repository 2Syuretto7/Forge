import numpy as np


def model(theta, x):
    """E + A x^(-alpha)."""
    raise NotImplementedError


def jacobian(theta, x):
    """Derivatives of the model in E, A and alpha."""
    raise NotImplementedError


def gauss_newton(x, y, theta0, iters=50):
    """Gauss-Newton iterations for the power law with a floor."""
    raise NotImplementedError
