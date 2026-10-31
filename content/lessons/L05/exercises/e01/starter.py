import numpy as np


def quad_fg(A, b, x):
    """f(x) = 0.5 x^T A x - b^T x and its gradient, for symmetric A."""
    raise NotImplementedError


def gd(grad, x0, lr, steps):
    """Gradient descent from x0. Return all iterates, shape (steps + 1, d)."""
    raise NotImplementedError
