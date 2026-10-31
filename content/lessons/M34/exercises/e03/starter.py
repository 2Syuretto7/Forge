import numpy as np


def dot_products(d, n, rng):
    """n dot products of independent standard normal vectors."""
    raise NotImplementedError


def score_variance(d, n, rng, scaled):
    """Variance of attention scores with or without the 1/sqrt(d) scale."""
    raise NotImplementedError


def variance_ratio(ds, n, rng):
    """Unscaled score variance divided by d, for each d."""
    raise NotImplementedError
