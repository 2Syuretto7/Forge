import math


def secant(f, x0, x1, tol=1e-14, max_iter=100):
    """(root, iterates) by the secant method."""
    raise NotImplementedError


def order_estimates(errors):
    """ln(e_{k+1}/e_k) / ln(e_k/e_{k-1}) over the usable errors."""
    raise NotImplementedError
