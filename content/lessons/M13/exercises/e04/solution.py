import numpy as np


def diagonalize(A):
    """(eigenvectors as columns, eigenvalues)."""
    lam, V = np.linalg.eig(A)
    return V, lam


def power_by_eig(A, k):
    """A^k through the eigen-decomposition."""
    V, lam = diagonalize(A)
    return np.real_if_close(V @ np.diag(lam ** k) @ np.linalg.inv(V), tol=1000)


def spectral(S):
    """(orthonormal eigenvectors, eigenvalues) of a symmetric matrix."""
    lam, Q = np.linalg.eigh(S)
    return Q, lam
