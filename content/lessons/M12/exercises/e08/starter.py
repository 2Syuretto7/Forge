import numpy as np


def coefficients(Q, b):
    """Q^T b."""
    raise NotImplementedError


def project_orthonormal(Q, b):
    """Q Q^T b."""
    raise NotImplementedError


def energy_split(Q, b):
    """(||Q^T b||^2, ||b - Q Q^T b||^2)."""
    raise NotImplementedError
