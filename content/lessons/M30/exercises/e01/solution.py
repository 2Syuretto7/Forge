import numpy as np


def min_norm(A, b):
    """Minimum-norm solution of A x = b and its Lagrange multipliers."""
    A = np.asarray(A, dtype=float)
    lam = -np.linalg.solve(A @ A.T, np.asarray(b, dtype=float))
    return -A.T @ lam, lam


def check_stationarity(A, x, lam):
    """Norm of the gradient of the Lagrangian in x."""
    return float(np.linalg.norm(np.asarray(x) + np.asarray(A).T @ lam))
