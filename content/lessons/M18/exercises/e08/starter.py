import numpy as np


def rayleigh(S, x):
    """x^T S x / x^T x."""
    raise NotImplementedError


def rayleigh_grad(S, x):
    """Gradient of the Rayleigh quotient."""
    raise NotImplementedError


def ascend(S, x0, lr, steps):
    """Gradient ascent with renormalization."""
    raise NotImplementedError
