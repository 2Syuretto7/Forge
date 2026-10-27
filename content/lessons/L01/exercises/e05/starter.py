import numpy as np


def lstsq_normal(A, b):
    """Return x (n,) solving the normal equations."""
    raise NotImplementedError


def lstsq_qr(A, b):
    """Return x (n,) using the QR factorization of A."""
    raise NotImplementedError


def residual_report(A, b, x):
    """Return {"residual_norm": float, "max_orthogonality": float}."""
    raise NotImplementedError
