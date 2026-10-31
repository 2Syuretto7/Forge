import numpy as np


def mean_and_cov(X):
    """(mean vector, sample covariance with n - 1)."""
    X = np.asarray(X, dtype=float)
    m = X.mean(axis=0)
    Xc = X - m
    return m, Xc.T @ Xc / (len(X) - 1)


def var_of_combination(cov, a):
    """Var(a^T x)."""
    a = np.asarray(a, dtype=float)
    return float(a @ np.asarray(cov, dtype=float) @ a)


def affine_moments(mu, cov, A, b):
    """Mean and covariance of A x + b."""
    A = np.asarray(A, dtype=float)
    return A @ np.asarray(mu, dtype=float) + np.asarray(b, dtype=float), A @ np.asarray(cov, dtype=float) @ A.T


def correlation_matrix(cov):
    """Correlations from a covariance matrix."""
    cov = np.asarray(cov, dtype=float)
    s = np.sqrt(np.diag(cov))
    return cov / np.outer(s, s)
