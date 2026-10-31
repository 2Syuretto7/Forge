import numpy as np


def vandermonde(m, n):
    """Polynomial design matrix on m equally spaced points in [0, 1]."""
    raise NotImplementedError


def solve_normal(A, b):
    """Least squares by the normal equations."""
    raise NotImplementedError


def solve_qr(A, b):
    """Least squares by QR."""
    raise NotImplementedError


def relative_error(x, x_true):
    """Relative error in the 2-norm."""
    raise NotImplementedError
