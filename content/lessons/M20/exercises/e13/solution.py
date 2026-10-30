import math

import numpy as np


def _phi(x):
    return math.exp(-x * x / 2) / math.sqrt(2 * math.pi)


def wrong_density(y):
    """Without the Jacobian factor."""
    return _phi((y - 1) / 2)


def right_density(y):
    """With the factor 1/2."""
    return _phi((y - 1) / 2) / 2


def total(density, lo=-30, hi=30, n=60_000):
    """Midpoint-rule integral."""
    h = (hi - lo) / n
    return sum(density(lo + h * (k + 0.5)) for k in range(n)) * h


def linear_density(y, A):
    """Density of A x for a standard normal pair x."""
    x = np.linalg.solve(A, y)
    return float(math.exp(-0.5 * x @ x) / (2 * math.pi) / abs(np.linalg.det(A)))
