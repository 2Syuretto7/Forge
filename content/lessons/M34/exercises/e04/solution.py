import math
import numpy as np


def jl_matrix(d, k, rng):
    """Gaussian projection matrix with N(0, 1/k) entries."""
    return rng.standard_normal((d, k)) / math.sqrt(k)


def pairwise_sq_dists(X):
    """Squared distances between all rows."""
    sq = np.sum(X * X, axis=1)
    return np.maximum(sq[:, None] + sq[None, :] - 2 * X @ X.T, 0.0)


def max_sq_distortion(X, Y):
    """Largest relative change of a squared pairwise distance."""
    i, j = np.triu_indices(len(X), 1)
    return float(np.max(np.abs(pairwise_sq_dists(Y)[i, j] / pairwise_sq_dists(X)[i, j] - 1)))


def jl_dim(n, eps):
    """Target dimension of the Johnson-Lindenstrauss lemma."""
    return math.ceil(4 * math.log(n) / (eps**2 / 2 - eps**3 / 3))
