import numpy as np


def vandermonde(m, n):
    """Polynomial design matrix on m equally spaced points in [0, 1]."""
    return np.vander(np.linspace(0, 1, m), n, increasing=True)


def solve_normal(A, b):
    """Least squares by the normal equations."""
    return np.linalg.solve(A.T @ A, A.T @ b)


def solve_qr(A, b):
    """Least squares by QR."""
    Q, R = np.linalg.qr(A)
    return np.linalg.solve(R, Q.T @ b)


def relative_error(x, x_true):
    """Relative error in the 2-norm."""
    return float(np.linalg.norm(np.asarray(x) - x_true) / np.linalg.norm(x_true))
