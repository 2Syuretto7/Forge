import numpy as np


def random_vectors(n, d, rng):
    """n standard normal vectors in d dimensions."""
    raise NotImplementedError


def norm_stats(d, n, rng):
    """(mean of |x| / sqrt(d), standard deviation of |x|)."""
    raise NotImplementedError


def shell_fraction(d, n, rng, width=0.1):
    """Fraction of lengths within width * sqrt(d) of sqrt(d)."""
    raise NotImplementedError
