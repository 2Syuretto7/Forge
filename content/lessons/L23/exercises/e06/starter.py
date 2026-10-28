import numpy as np


def random_unit_vectors(n, d, seed=0):
    """n random directions in d dimensions, as rows of unit length."""
    raise NotImplementedError


def mean_interference(V):
    """The mean squared cosine between distinct rows: how much reading one feature's direction
    picks up the others."""
    raise NotImplementedError


def max_interference(V):
    """The largest absolute cosine between distinct rows."""
    raise NotImplementedError
