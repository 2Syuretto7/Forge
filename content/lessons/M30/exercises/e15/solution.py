import itertools
import numpy as np


def brute_force(W):
    """Minimum of x^T W x over sign vectors."""
    W = np.asarray(W, dtype=float)
    S = np.array(list(itertools.product([-1.0, 1.0], repeat=W.shape[0])))
    return float(np.min(np.einsum("ki,ij,kj->k", S, W, S)))


def eigen_bound(W):
    """n times the smallest eigenvalue: a Lagrangian lower bound."""
    W = np.asarray(W, dtype=float)
    return float(W.shape[0] * np.linalg.eigvalsh(W)[0])


def gap(W):
    """Duality gap p* - d."""
    return brute_force(W) - eigen_bound(W)
