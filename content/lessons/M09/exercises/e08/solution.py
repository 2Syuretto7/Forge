import numpy as np


def random_cosines(d, n, seed=0):
    """Cosines of n random pairs in d dimensions."""
    rng = np.random.default_rng(seed)
    a, b = rng.normal(size=(n, d)), rng.normal(size=(n, d))
    return np.sum(a * b, axis=1) / (np.linalg.norm(a, axis=1) * np.linalg.norm(b, axis=1))


def typical_cosine(d, n=4000):
    """Standard deviation of random cosines."""
    return float(np.std(random_cosines(d, n)))


def fraction_nearly_perpendicular(d, tol, n=4000):
    """Fraction of random pairs with |cos| < tol."""
    return float(np.mean(np.abs(random_cosines(d, n)) < tol))
