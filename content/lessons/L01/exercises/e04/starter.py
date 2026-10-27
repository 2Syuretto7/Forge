import numpy as np


def qr(A):
    """A: (m, n), m >= n. Return Q (m, n) orthonormal, R (n, n) upper triangular, diag(R) > 0."""
    raise NotImplementedError


def back_substitute(R, y):
    """Solve R x = y for upper-triangular R (n, n). Return x (n,)."""
    raise NotImplementedError
