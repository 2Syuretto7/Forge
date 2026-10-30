import numpy as np


def determinants(A):
    """Determinants of an (n, 2, 2) array of matrices."""
    return A[:, 0, 0] * A[:, 1, 1] - A[:, 0, 1] * A[:, 1, 0]


def solve_many(A, rhs):
    """Solutions (n, 2) of n 2x2 systems by elimination, without a Python loop."""
    a, b, c, d = A[:, 0, 0], A[:, 0, 1], A[:, 1, 0], A[:, 1, 1]
    p, q = rhs[:, 0], rhs[:, 1]
    det = a * d - b * c
    return np.stack([(p * d - b * q) / det, (a * q - c * p) / det], axis=1)
