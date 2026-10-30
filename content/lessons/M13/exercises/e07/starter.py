import numpy as np


def transition_matrix(C):
    """Columns of counts normalized to sum to 1."""
    raise NotImplementedError


def stationary_power(P, tol=1e-12, max_iter=100000):
    """Iterate p <- P p from the uniform distribution."""
    raise NotImplementedError


def stationary_eig(P):
    """Eigenvector of the eigenvalue nearest 1, summing to 1."""
    raise NotImplementedError
