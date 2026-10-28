import numpy as np


def random_unit_vectors(n, d, seed=0):
    """n random directions in d dimensions, as rows of unit length."""
    V = np.random.default_rng(seed).normal(size=(n, d))
    return V / np.linalg.norm(V, axis=1, keepdims=True)


def mean_interference(V):
    """The mean squared cosine between distinct rows: how much reading one feature's direction
    picks up the others."""
    G = V @ V.T
    n = len(V)
    return float((np.sum(G ** 2) - n) / (n * (n - 1)))


def max_interference(V):
    """The largest absolute cosine between distinct rows."""
    G = np.abs(V @ V.T)
    np.fill_diagonal(G, 0)
    return float(G.max())
