import numpy as np


def coefficients(Q, b):
    """Q^T b."""
    return Q.T @ b


def project_orthonormal(Q, b):
    """Q Q^T b."""
    return Q @ (Q.T @ b)


def energy_split(Q, b):
    """(||Q^T b||^2, ||b - Q Q^T b||^2)."""
    c = Q.T @ b
    r = b - Q @ c
    return float(c @ c), float(r @ r)
