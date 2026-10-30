import numpy as np


def naive_cosine(x, y):
    """x . y / (|x| |y|), nan for a zero vector."""
    with np.errstate(all="ignore"):
        return float(x @ y / (np.linalg.norm(x) * np.linalg.norm(y)))


def safe_cosine(x, y, eps=1e-12):
    """Cosine, or ValueError if either vector is (nearly) zero."""
    nx, ny = np.linalg.norm(x), np.linalg.norm(y)
    if nx < eps or ny < eps:
        raise ValueError("cosine with a zero vector is undefined")
    return float(x @ y / (nx * ny))


def normalize_rows_safe(X, eps=1e-12):
    """(normalized rows with tiny rows left at zero, indices of the tiny rows)."""
    n = np.linalg.norm(X, axis=1)
    bad = np.flatnonzero(n < eps)
    U = X / np.where(n < eps, 1.0, n)[:, None]
    U[bad] = 0.0
    return U, [int(i) for i in bad]
