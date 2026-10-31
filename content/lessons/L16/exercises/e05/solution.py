import numpy as np


def best_rank_r(M, r):
    """The rank-r matrix closest to M in Frobenius norm: the truncated SVD (Eckart-Young)."""
    U, S, Vt = np.linalg.svd(M, full_matrices=False)
    return (U[:, :r] * S[:r]) @ Vt[:r]


def relative_error(M, r):
    """|M - best_rank_r(M, r)|_F / |M|_F, from the singular values alone."""
    S = np.linalg.svd(M, compute_uv=False)
    return float(np.sqrt(np.sum(S[r:] ** 2) / np.sum(S ** 2)))


def rank_for(M, tol):
    """The smallest rank whose relative error is at most tol."""
    for r in range(min(M.shape) + 1):
        if relative_error(M, r) <= tol:
            return r
