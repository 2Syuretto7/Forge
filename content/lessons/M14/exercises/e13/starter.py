import numpy as np


# provided
def make_offset_cloud(seed=0):
    rng = np.random.default_rng(seed)
    true_dir = rng.normal(size=10)
    true_dir /= np.linalg.norm(true_dir)
    mean = 20 * rng.normal(size=10)
    X = mean + np.outer(3 * rng.normal(size=500), true_dir) + 0.3 * rng.normal(size=(500, 10))
    return X, true_dir


def first_direction(X, centre):
    """Top right singular vector, with or without centring."""
    raise NotImplementedError


def alignment(u, v):
    """|u . v| for unit vectors."""
    raise NotImplementedError


def explained_first(X, centre):
    """sigma_1^2 / sum sigma_i^2."""
    raise NotImplementedError
