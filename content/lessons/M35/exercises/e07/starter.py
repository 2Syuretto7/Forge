import numpy as np


def model(theta, x):
    """E + A x^(-alpha)."""
    raise NotImplementedError


def jacobian(theta, x):
    """Derivatives of the model in E, A and alpha."""
    raise NotImplementedError


def fit(x, y, theta0, iters=60):
    """Levenberg-Marquardt fit."""
    raise NotImplementedError


def residual_bootstrap(x, y, theta_hat, B, rng):
    """Refits on datasets built from resampled residuals."""
    raise NotImplementedError


def percentile_interval(samples, level=0.95):
    """Percentile interval of each column."""
    raise NotImplementedError
