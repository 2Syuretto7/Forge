import numpy as np


def var_sum_independent(cov):
    """Variance of the sum if the terms were independent."""
    raise NotImplementedError


def var_sum(cov):
    """Variance of the sum: the sum of all covariances."""
    raise NotImplementedError


def equicorrelated(n, rho, sigma=1.0):
    """Covariance matrix with equal variances and equal correlations."""
    raise NotImplementedError


def effective_n(n, rho):
    """Number of independent samples worth n equicorrelated ones."""
    raise NotImplementedError
