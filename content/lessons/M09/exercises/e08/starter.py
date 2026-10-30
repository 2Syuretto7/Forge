import numpy as np


def random_cosines(d, n, seed=0):
    """Cosines of n random pairs in d dimensions."""
    raise NotImplementedError


def typical_cosine(d, n=4000):
    """Standard deviation of random cosines."""
    raise NotImplementedError


def fraction_nearly_perpendicular(d, tol, n=4000):
    """Fraction of random pairs with |cos| < tol."""
    raise NotImplementedError
