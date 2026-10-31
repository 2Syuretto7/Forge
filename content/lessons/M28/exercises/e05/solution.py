import numpy as np


def smooth_strong(A):
    """(L, mu) of the quadratic with Hessian A."""
    w = np.linalg.eigvalsh(np.asarray(A, dtype=float))
    return float(w[-1]), float(w[0])


def condition_number(A):
    """L / mu."""
    L, mu = smooth_strong(A)
    return L / mu


def logistic_smoothness(X):
    """Upper bound on the smoothness of the average logistic loss."""
    X = np.asarray(X, dtype=float)
    return float(np.linalg.eigvalsh(X.T @ X)[-1] / (4 * len(X)))


def level_set_axes(A, c=1.0):
    """Half-axes of the level set (1/2) x^T A x = c, longest first."""
    w = np.linalg.eigvalsh(np.asarray(A, dtype=float))
    return np.sqrt(2 * c / w)
