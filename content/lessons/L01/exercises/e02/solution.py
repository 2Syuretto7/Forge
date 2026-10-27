import numpy as np


def project_onto_line(b, a):
    """b, a: shape (m,). Return the projection of b onto span{a}, shape (m,)."""
    a = np.asarray(a, dtype=float)
    return (a @ b) / (a @ a) * a


def projection_matrix(A):
    """A: shape (m, n), independent columns. Return P, shape (m, m)."""
    A = np.asarray(A, dtype=float)
    return A @ np.linalg.solve(A.T @ A, A.T)


def project(b, A):
    """Return the projection of b (shape (m,)) onto the column space of A."""
    A = np.asarray(A, dtype=float)
    x = np.linalg.solve(A.T @ A, A.T @ b)
    return A @ x
