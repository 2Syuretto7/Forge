import numpy as np


def quadratic(A, b, x):
    """f(x) = x^T A x / 2 - b^T x."""
    raise NotImplementedError


def grad_quadratic(A, b, x):
    """Gradient of the quadratic."""
    raise NotImplementedError


def cg(matvec, b, tol=1e-10, max_iter=None):
    """Conjugate gradient from zero: (x, residual norms, directions)."""
    raise NotImplementedError
