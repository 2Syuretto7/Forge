import numpy as np


def leverages(A):
    """Diagonal of the projection matrix."""
    Q, _ = np.linalg.qr(A)
    return np.sum(Q * Q, axis=1)


def line_design(x):
    """Columns 1 and x."""
    x = np.asarray(x, dtype=float)
    return np.column_stack([np.ones_like(x), x])


def _slope(x, y):
    c, *_ = np.linalg.lstsq(line_design(x), y, rcond=None)
    return c[1]


def influence(x, y, i):
    """Slope without point i minus slope with it."""
    return float(_slope(np.delete(x, i), np.delete(y, i)) - _slope(x, y))
