import numpy as np


def f(x):
    """Tilted double well."""
    raise NotImplementedError


def fprime(x):
    """Its derivative."""
    raise NotImplementedError


def descend(x0, step=0.01, iters=5000):
    """Gradient descent from x0."""
    raise NotImplementedError


def basin_fraction(starts):
    """Fraction of starts that reach the global minimum."""
    raise NotImplementedError


def _root(lo, hi):
    raise NotImplementedError


def minima():
    """The two local minima, sorted."""
    raise NotImplementedError
