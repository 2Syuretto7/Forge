import numpy as np


def central_vec(f, x, h):
    """Elementwise central differences."""
    return (f(x + h) - f(x - h)) / (2 * h)


def max_rel_error(est, exact):
    """Largest relative error."""
    return float(np.max(np.abs(est - exact) / np.abs(exact)))


def compare_steps(n=1_000_000):
    """(max relative error with h = 1e-5, with the scaled step) for log."""
    x = np.logspace(-3, 3, n)
    exact = 1 / x
    fixed = max_rel_error(central_vec(np.log, x, 1e-5), exact)
    h = np.finfo(float).eps ** (1 / 3) * np.abs(x)
    scaled = max_rel_error(central_vec(np.log, x, h), exact)
    return fixed, scaled
