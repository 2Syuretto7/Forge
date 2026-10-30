import numpy as np


def gram(X):
    """Table of dot products of the rows."""
    return X @ X.T


def quadratic_form(G, z):
    """z^T G z."""
    return float(z @ G @ z)


def as_squared_length(X, z):
    """Squared length of sum z_i x_i."""
    v = z @ X
    return float(v @ v)
