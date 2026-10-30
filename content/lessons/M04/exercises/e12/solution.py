import math

import numpy as np


def sqrt_error(n):
    """Largest error of the n-piece interpolant of sqrt on [0, 1]."""
    x = np.linspace(0, 1, 20001)
    knots = np.linspace(0, 1, n + 1)
    return float(np.max(np.abs(np.sqrt(x) - np.interp(x, knots, np.sqrt(knots)))))


def predicted_sqrt_error(n):
    """sqrt(h) / 4 with h = 1/n."""
    return math.sqrt(1 / n) / 4


def pieces_for_sqrt(tol):
    """Smallest n with predicted_sqrt_error(n) <= tol."""
    n = math.ceil(1 / (16 * tol * tol) - 1e-9)
    while predicted_sqrt_error(n) > tol:
        n += 1
    return n
