import numpy as np


def dot_products(d, n, rng):
    """n dot products of independent standard normal vectors."""
    return np.einsum("ij,ij->i", rng.standard_normal((n, d)), rng.standard_normal((n, d)))


def score_variance(d, n, rng, scaled):
    """Variance of attention scores with or without the 1/sqrt(d) scale."""
    s = dot_products(d, n, rng)
    if scaled:
        s = s / np.sqrt(d)
    return float(np.var(s))


def variance_ratio(ds, n, rng):
    """Unscaled score variance divided by d, for each d."""
    return [score_variance(d, n, rng, False) / d for d in ds]
