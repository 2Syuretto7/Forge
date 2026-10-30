import numpy as np


def pinv(A, rtol=1e-12):
    """Moore-Penrose pseudo-inverse via the SVD."""
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    if s.size == 0 or s[0] == 0:
        return np.zeros((A.shape[1], A.shape[0]))
    s_inv = np.where(s > rtol * s[0], 1 / np.where(s > 0, s, 1), 0.0)
    return (Vt.T * s_inv) @ U.T


def min_norm_solution(A, b):
    """Least-squares solution of smallest length."""
    return pinv(A) @ b
