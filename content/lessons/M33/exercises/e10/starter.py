import numpy as np


# provided
def make_matrix(m, n, decay, rng):
    U = np.linalg.qr(rng.standard_normal((m, n)))[0]
    V = np.linalg.qr(rng.standard_normal((n, n)))[0]
    return (U / np.arange(1, n + 1) ** decay) @ V.T


def _rsvd(A, k, p, q, rng):
    raise NotImplementedError


def relative_errors(A, ks, p, q, rng):
    """Relative Frobenius errors of randomized SVDs of each rank."""
    raise NotImplementedError


def optimal_errors(s, ks):
    """Relative Frobenius errors of truncated SVDs."""
    raise NotImplementedError


def matvecs(k, p, q):
    """Products of A or A^T with vectors."""
    raise NotImplementedError
