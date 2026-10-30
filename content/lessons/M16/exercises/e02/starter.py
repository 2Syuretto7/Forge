import math


def bisect(f, a, b, tol=1e-12, max_iter=200):
    """(root, iterations) by halving a sign-changing bracket."""
    raise NotImplementedError


def predicted_iterations(a, b, tol):
    """ceil(log2((b - a) / tol))."""
    raise NotImplementedError
