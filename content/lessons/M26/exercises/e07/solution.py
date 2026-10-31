import numpy as np


def softplus(x):
    """log(1 + e^x), stably."""
    x = np.asarray(x, dtype=float)
    return np.maximum(x, 0) + np.log1p(np.exp(-np.abs(x)))


def sigmoid(x):
    """1 / (1 + e^-x), stably for both signs."""
    x = np.asarray(x, dtype=float)
    e = np.exp(-np.abs(x))
    return np.where(x >= 0, 1 / (1 + e), e / (1 + e))


def log_sigmoid(x):
    """log(sigmoid(x)), stably."""
    return -softplus(-np.asarray(x, dtype=float))
