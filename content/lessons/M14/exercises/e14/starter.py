import numpy as np


def ill_matrix(kappa, seed=0):
    """40 x 6 matrix with singular values from 1 to 1/kappa."""
    raise NotImplementedError


def smallest_two_ways(A):
    """(smallest singular value from the SVD, from eig of A^T A)."""
    raise NotImplementedError


def normal_vs_qr(A, x_true):
    """Relative errors of the normal equations and QR."""
    raise NotImplementedError
