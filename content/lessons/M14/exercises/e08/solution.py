import numpy as np


def column_space_basis(A, rtol=1e-10):
    """Orthonormal basis of col(A) from the SVD."""
    U, s, _ = np.linalg.svd(A, full_matrices=False)
    r = int(np.sum(s > rtol * s[0])) if s.size and s[0] > 0 else 0
    return U[:, :r]


def project_svd(b, A):
    """Projection of b onto col(A)."""
    Ur = column_space_basis(A)
    return Ur @ (Ur.T @ b)
