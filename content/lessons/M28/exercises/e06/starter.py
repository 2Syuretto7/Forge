import numpy as np


def make_quadratic(eigs, seed):
    """Symmetric matrix with the given eigenvalues and random eigenvectors."""
    raise NotImplementedError


def gd_errors(A, b, x0, step, iters):
    """Error norms of gradient descent on (1/2) x^T A x - b^T x."""
    raise NotImplementedError


def rate(eigs, step):
    """Worst contraction factor of gradient descent."""
    raise NotImplementedError
