import numpy as np


def rayleigh(S, x):
    """Return x^T S x / x^T x as a float."""
    raise NotImplementedError


def rayleigh_grad(S, x):
    """Return the gradient of the Rayleigh quotient at x, shape (n,)."""
    raise NotImplementedError


def ascend(S, x0, lr, steps):
    """Gradient ascent with renormalization. Return a unit vector (n,)."""
    raise NotImplementedError
