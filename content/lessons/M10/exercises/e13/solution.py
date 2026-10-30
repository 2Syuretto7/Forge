from functools import reduce

import numpy as np


# provided
def _t(tx, ty):
    return np.array([[1.0, 0, tx], [0, 1.0, ty], [0, 0, 1.0]])


# provided
def _r(theta):
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s, 0], [s, c, 0], [0, 0, 1.0]])


def pipeline_matrix(steps):
    """One matrix for steps applied in order."""
    return reduce(lambda acc, M: M @ acc, steps[1:], steps[0])


def commutes(A, B, tol=1e-12):
    """Whether AB = BA up to tol."""
    return bool(np.max(np.abs(A @ B - B @ A)) <= tol)


def place_logo():
    """Rotate the unit square 45 degrees about its centre, then centre it at (3, 2)."""
    return [_t(-0.5, -0.5), _r(np.pi / 4), _t(0.5, 0.5), _t(2.5, 1.5)]
