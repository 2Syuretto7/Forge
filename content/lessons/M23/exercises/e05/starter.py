import numpy as np


def sample(mu, Sigma, n, rng):
    """n samples of N(mu, Sigma) by the Cholesky factor."""
    raise NotImplementedError


def whiten(X):
    """Cholesky whitening with the sample mean and covariance."""
    raise NotImplementedError


def zca(X):
    """Symmetric (ZCA) whitening."""
    raise NotImplementedError
