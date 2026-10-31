import numpy as np


def mean_and_cov(X):
    """(mean vector, sample covariance with n - 1)."""
    raise NotImplementedError


def var_of_combination(cov, a):
    """Var(a^T x)."""
    raise NotImplementedError


def affine_moments(mu, cov, A, b):
    """Mean and covariance of A x + b."""
    raise NotImplementedError


def correlation_matrix(cov):
    """Correlations from a covariance matrix."""
    raise NotImplementedError
