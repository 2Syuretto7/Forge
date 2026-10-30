import math

import numpy as np


def is_eigenpair(A, lam, v, tol=1e-9):
    """Whether A v = lam v (v nonzero) up to a relative tolerance."""
    v = np.asarray(v, dtype=float)
    if not np.any(v):
        return False
    scale = max(1.0, np.linalg.norm(A) * np.linalg.norm(v))
    return bool(np.linalg.norm(A @ v - lam * v) <= tol * scale)


def char_poly2(A):
    """(1, -trace, det)."""
    (a, b), (c, d) = A
    return (1.0, -(a + d), a * d - b * c)


def eig2_real(A):
    """Real eigenvalues of a 2 by 2 matrix, larger first."""
    _, p, q = char_poly2(A)
    disc = p * p - 4 * q
    if disc < 0:
        raise ValueError("complex eigenvalues")
    s = math.sqrt(disc)
    return ((-p + s) / 2, (-p - s) / 2)
