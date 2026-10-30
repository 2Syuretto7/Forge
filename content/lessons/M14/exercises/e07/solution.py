import numpy as np


def cond2(A):
    """Return sigma_max / sigma_min for square A."""
    s = np.linalg.svd(A, compute_uv=False)
    return float(s[0] / s[-1])


def amplification(A, b, db):
    """Return (|dx| / |x|) / (|db| / |b|) for A x = b and A dx = db."""
    x = np.linalg.solve(A, b)
    dx = np.linalg.solve(A, db)
    return float((np.linalg.norm(dx) / np.linalg.norm(x)) / (np.linalg.norm(db) / np.linalg.norm(b)))


def worst_case_pair(A):
    """Return unit vectors (b, db) whose amplification equals cond2(A)."""
    U, _, _ = np.linalg.svd(A)
    return U[:, 0].copy(), U[:, -1].copy()
