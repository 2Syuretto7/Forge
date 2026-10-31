import numpy as np


def ito_sum(W):
    """Left-point Riemann sum of W dW."""
    W = np.asarray(W)
    return float(np.sum(W[:-1] * np.diff(W)))


def midpoint_sum(W):
    """Averaged-endpoint sum of W dW."""
    W = np.asarray(W)
    return float(np.sum(0.5 * (W[:-1] + W[1:]) * np.diff(W)))


def quadratic_variation(W):
    """Sum of squared increments."""
    return float(np.sum(np.diff(np.asarray(W)) ** 2))
