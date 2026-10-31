import numpy as np


def best_rank_r(M, r):
    """Truncated SVD of rank r."""
    U, s, Vt = np.linalg.svd(np.asarray(M), full_matrices=False)
    return (U[:, :r] * s[:r]) @ Vt[:r]


def rank_r_error(M, r):
    """Relative Frobenius error of the best rank-r approximation."""
    return float(np.linalg.norm(M - best_rank_r(M, r)) / np.linalg.norm(M))


def effective_rank(M, energy=0.9):
    """Smallest rank capturing the given fraction of the squared singular values."""
    s2 = np.linalg.svd(np.asarray(M), compute_uv=False) ** 2
    return int(np.searchsorted(np.cumsum(s2) / s2.sum(), energy) + 1)
