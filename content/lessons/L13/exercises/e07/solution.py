import numpy as np


def rope(X, positions, base=10000.0):
    """Rotate each pair of features (2i, 2i+1) of row p by the angle p * theta_i, with
    theta_i = base^(-2i/d). X has shape (n, d) with d even; positions has shape (n,)."""
    n, d = X.shape
    theta = base ** (-2 * np.arange(d // 2) / d)
    ang = np.asarray(positions, dtype=float)[:, None] * theta[None, :]
    c, s = np.cos(ang), np.sin(ang)
    x0, x1 = X[:, 0::2], X[:, 1::2]
    out = np.empty_like(X, dtype=float)
    out[:, 0::2] = x0 * c - x1 * s
    out[:, 1::2] = x0 * s + x1 * c
    return out
