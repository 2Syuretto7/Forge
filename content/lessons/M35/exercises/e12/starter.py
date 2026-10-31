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


def extrapolation_trial(x, theta_true, sigma, x0s, rng):
    """Prediction errors and delta-method standard errors at x0s for one dataset."""
    raise NotImplementedError


def coverage(errors, ses, z=1.96):
    """Fraction of trials whose error lies inside the band."""
    raise NotImplementedError


def rms_error(errors):
    """Root-mean-square error per column."""
    raise NotImplementedError
