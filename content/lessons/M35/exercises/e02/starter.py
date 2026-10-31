import numpy as np


def fit_loglog(x, y):
    """(A, alpha) from least squares on the logarithms."""
    raise NotImplementedError


def loglog_r2(x, y):
    """R^2 of the log-log linear fit."""
    raise NotImplementedError


def predict_loglog(A, alpha, x):
    """Prediction of the fitted power law."""
    raise NotImplementedError
