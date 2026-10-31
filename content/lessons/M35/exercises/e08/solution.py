import numpy as np


def prediction(theta, x0):
    """E + A x0^(-alpha)."""
    E, A, alpha = theta
    return E + A * x0 ** (-alpha)


def grad_prediction(theta, x0):
    """Gradient of the prediction in (E, A, alpha)."""
    _, A, alpha = theta
    p = x0 ** (-alpha)
    return np.array([1.0, p, -A * p * np.log(x0)])


def prediction_se(theta, cov, x0):
    """Delta-method standard error of the prediction."""
    g = grad_prediction(theta, x0)
    return float(np.sqrt(g @ cov @ g))


def band(theta, cov, xs, z=1.96):
    """Pointwise band of half-width z standard errors."""
    p = np.array([prediction(theta, x) for x in xs])
    s = np.array([prediction_se(theta, cov, x) for x in xs])
    return p - z * s, p + z * s
