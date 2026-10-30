import math


def one_sided(f, a, h=1e-7):
    """(left slope, right slope)."""
    raise NotImplementedError


def has_corner(f, a, h=1e-7, tol=1e-4):
    """Whether the one-sided slopes differ."""
    raise NotImplementedError


def relu_grad(x):
    """Framework convention: 1 if x > 0 else 0."""
    raise NotImplementedError


def abs_subgradients(x):
    """Interval of subgradients of |x|."""
    raise NotImplementedError
