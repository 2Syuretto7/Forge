import numpy as np


def mp_edges(gamma):
    """Edges of the Marchenko-Pastur support."""
    raise NotImplementedError


def mp_density(x, gamma):
    """Marchenko-Pastur density for variance 1 and ratio gamma <= 1."""
    raise NotImplementedError


def sample_cov_eigs(n, p, rng):
    """Eigenvalues of the sample covariance of n standard normal samples."""
    raise NotImplementedError


def mp_moments(gamma):
    """First two moments of the Marchenko-Pastur law."""
    raise NotImplementedError
