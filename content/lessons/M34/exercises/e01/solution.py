import numpy as np


def random_vectors(n, d, rng):
    """n standard normal vectors in d dimensions."""
    return rng.standard_normal((n, d))


def norm_stats(d, n, rng):
    """(mean of |x| / sqrt(d), standard deviation of |x|)."""
    r = np.linalg.norm(random_vectors(n, d, rng), axis=1)
    return float(np.mean(r) / np.sqrt(d)), float(np.std(r))


def shell_fraction(d, n, rng, width=0.1):
    """Fraction of lengths within width * sqrt(d) of sqrt(d)."""
    r = np.linalg.norm(random_vectors(n, d, rng), axis=1)
    return float(np.mean(np.abs(r - np.sqrt(d)) <= width * np.sqrt(d)))
