import numpy as np


def complement_basis(A):
    """Orthonormal basis of the complement of col(A)."""
    Q, _ = np.linalg.qr(A, mode="complete")
    return Q[:, A.shape[1]:]


def split(b, A):
    """(p, r): b = p + r, p in col(A), r perpendicular to it."""
    p = A @ np.linalg.solve(A.T @ A, A.T @ b)
    return p, b - p
