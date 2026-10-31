import numpy as np


def fit_loglog(x, y):
    """(A, alpha) from least squares on the logarithms."""
    slope, intercept = np.polyfit(np.log(x), np.log(y), 1)
    return float(np.exp(intercept)), float(-slope)


def loglog_r2(x, y):
    """R^2 of the log-log linear fit."""
    u, v = np.log(x), np.log(y)
    slope, intercept = np.polyfit(u, v, 1)
    res = v - (slope * u + intercept)
    return float(1 - res @ res / np.sum((v - v.mean()) ** 2))


def predict_loglog(A, alpha, x):
    """Prediction of the fitted power law."""
    return A * np.asarray(x, dtype=float) ** (-alpha)
