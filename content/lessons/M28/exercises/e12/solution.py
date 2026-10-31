import numpy as np


def jacobi(A):
    """Symmetric Jacobi preconditioning."""
    A = np.asarray(A, dtype=float)
    d = 1 / np.sqrt(np.diag(A))
    return A * np.outer(d, d)


def kappa(A):
    """Condition number of a symmetric positive definite matrix."""
    w = np.linalg.eigvalsh(np.asarray(A, dtype=float))
    return float(w[-1] / w[0])


def scaled_least_squares(n, scales, seed):
    """Hessian of least squares on features with the given scales."""
    X = np.random.default_rng(seed).standard_normal((n, len(scales))) * np.asarray(scales, dtype=float)
    return X.T @ X / n
