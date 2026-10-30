import numpy as np


def det2(A):
    """ad - bc."""
    (a, b), (c, d) = A
    return a * d - b * c


def det3(A):
    """Expansion along the first row."""
    A = np.asarray(A, dtype=float)
    total = 0.0
    for j in range(3):
        minor = np.delete(A[1:], j, axis=1)
        total += (-1) ** j * A[0, j] * det2(minor)
    return float(total)


def inverse2(A):
    """Inverse of a 2 by 2 matrix; ValueError if singular."""
    (a, b), (c, d) = A
    det = a * d - b * c
    if det == 0:
        raise ValueError("singular matrix")
    return np.array([[d, -b], [-c, a]]) / det
