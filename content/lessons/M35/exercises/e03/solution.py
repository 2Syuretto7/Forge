import numpy as np


def lognormal_mean_factor(sigma):
    """Mean over median of a lognormal variable."""
    return float(np.exp(sigma**2 / 2))


def naive_mean_prediction(A, alpha, x):
    """Exponentiated log-space fit: a median, not a mean."""
    return A * np.asarray(x, dtype=float) ** (-alpha)


def smearing_factor(residuals):
    """Duan's smearing correction."""
    return float(np.mean(np.exp(residuals)))


def log_residuals(x, y, A, alpha):
    """Residuals of the log-space fit."""
    return np.log(y) - np.log(A * np.asarray(x, dtype=float) ** (-alpha))
