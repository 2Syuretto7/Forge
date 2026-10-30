import numpy as np


def qr(A):
    """A = QR by modified Gram-Schmidt, diag(R) > 0."""
    raise NotImplementedError


def back_substitute(R, y):
    """Solve R x = y, R upper triangular."""
    raise NotImplementedError


def lstsq_qr(A, b):
    """Least squares through A = QR."""
    raise NotImplementedError
