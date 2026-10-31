import numpy as np


def is_psd(C, tol=1e-10):
    """Whether C has no eigenvalue below -tol."""
    raise NotImplementedError


def negative_variance_direction(C):
    """Unit vector minimizing a^T C a."""
    raise NotImplementedError


def nearest_correlation(C, eps=1e-6):
    """Clip eigenvalues and restore a unit diagonal."""
    raise NotImplementedError
