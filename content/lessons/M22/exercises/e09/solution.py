import numpy as np


def mse(c, values, probs):
    """E[(X - c)^2]."""
    values, probs = np.asarray(values, dtype=float), np.asarray(probs, dtype=float)
    return float(np.sum(probs * (values - c) ** 2))


def dmse_dc(c, values, probs):
    """Derivative of mse with respect to c."""
    values, probs = np.asarray(values, dtype=float), np.asarray(probs, dtype=float)
    return float(-2 * np.sum(probs * (values - c)))


def best_constant(values, probs):
    """The minimizer of mse: the mean."""
    return float(np.sum(np.asarray(values, dtype=float) * np.asarray(probs, dtype=float)))


def mae(c, values, probs):
    """E|X - c|."""
    values, probs = np.asarray(values, dtype=float), np.asarray(probs, dtype=float)
    return float(np.sum(probs * np.abs(values - c)))


def best_constant_abs(values, probs):
    """A median: the smallest sorted value with cumulative probability at least 1/2."""
    values, probs = np.asarray(values, dtype=float), np.asarray(probs, dtype=float)
    order = np.argsort(values)
    cum = np.cumsum(probs[order])
    return float(values[order][np.searchsorted(cum, 0.5 - 1e-12)])
