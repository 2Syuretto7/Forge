import numpy as np


def project_onto_line(b, a):
    """Projection of b onto the line through a."""
    a = np.asarray(a, dtype=float)
    return (a @ b) / (a @ a) * a


def projection_matrix(A):
    """P = A (A^T A)^-1 A^T."""
    A = np.asarray(A, dtype=float)
    return A @ np.linalg.solve(A.T @ A, A.T)


def project(b, A):
    """Projection of b onto the column space of A."""
    A = np.asarray(A, dtype=float)
    return A @ np.linalg.solve(A.T @ A, A.T @ b)
