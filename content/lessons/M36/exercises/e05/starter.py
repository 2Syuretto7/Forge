import numpy as np


def gumbel(shape, rng):
    """Standard Gumbel samples."""
    raise NotImplementedError


def gumbel_max(z, n, rng):
    """Categorical samples by the Gumbel-max trick."""
    raise NotImplementedError


def gumbel_softmax(z, tau, n, rng):
    """Relaxed one-hot samples."""
    raise NotImplementedError


def mean_max_entry(Y):
    """Average largest entry per row."""
    raise NotImplementedError
