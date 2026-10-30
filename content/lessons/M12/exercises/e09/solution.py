import numpy as np


def line_fit(x, y):
    """(w0, w1) from the 2 by 2 normal equations."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    a, b, c, d = len(x), x.sum(), x.sum(), (x * x).sum()
    p, q = y.sum(), (x * y).sum()
    det = a * d - b * c
    return (p * d - b * q) / det, (a * q - c * p) / det


def centered_fit(x, y):
    """(w0, w1) from deviations from the means."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    dx, dy = x - x.mean(), y - y.mean()
    w1 = (dx @ dy) / (dx @ dx)
    return y.mean() - w1 * x.mean(), w1


def residual_checks(x, y, w0, w1):
    """(sum r, sum x r)."""
    x, y = np.asarray(x, dtype=float), np.asarray(y, dtype=float)
    r = y - w0 - w1 * x
    return float(r.sum()), float(x @ r)
