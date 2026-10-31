import numpy as np


def jacobi(A):
    """Symmetric Jacobi preconditioning."""
    raise NotImplementedError


def kappa(A):
    """Condition number of a symmetric positive definite matrix."""
    raise NotImplementedError


def scaled_least_squares(n, scales, seed):
    """Hessian of least squares on features with the given scales."""
    raise NotImplementedError
