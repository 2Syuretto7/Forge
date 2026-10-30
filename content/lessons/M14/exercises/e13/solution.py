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
    Y = X - X.mean(axis=0) if centre else X
    return np.linalg.svd(Y, full_matrices=False)[2][0]


def alignment(u, v):
    """|u . v| for unit vectors."""
    return float(abs(u @ v))


def explained_first(X, centre):
    """sigma_1^2 / sum sigma_i^2."""
    Y = X - X.mean(axis=0) if centre else X
    s = np.linalg.svd(Y, compute_uv=False)
    return float(s[0] ** 2 / np.sum(s ** 2))
