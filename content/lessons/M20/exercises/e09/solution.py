import math

import numpy as np


def normalizer(Sigma):
    """(2 pi)^(n/2) sqrt(det Sigma)."""
    n = Sigma.shape[0]
    return (2 * math.pi) ** (n / 2) * math.sqrt(np.linalg.det(Sigma))


def gaussian_density(x, Sigma):
    """Multivariate normal density with mean 0."""
    return float(math.exp(-0.5 * x @ np.linalg.solve(Sigma, x)) / normalizer(Sigma))


def sample_gaussian(Sigma, n, seed=0):
    """Rows x = L z."""
    L = np.linalg.cholesky(Sigma)
    return np.random.default_rng(seed).normal(size=(n, Sigma.shape[0])) @ L.T
