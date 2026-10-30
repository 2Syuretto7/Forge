import numpy as np


def var_sum_independent(cov):
    """Variance of the sum if the terms were independent."""
    return float(np.trace(np.asarray(cov, dtype=float)))


def var_sum(cov):
    """Variance of the sum: the sum of all covariances."""
    return float(np.asarray(cov, dtype=float).sum())


def equicorrelated(n, rho, sigma=1.0):
    """Covariance matrix with equal variances and equal correlations."""
    return sigma**2 * ((1 - rho) * np.eye(n) + rho)


def effective_n(n, rho):
    """Number of independent samples worth n equicorrelated ones."""
    return n / (1 + (n - 1) * rho)
