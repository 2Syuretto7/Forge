import numpy as np


# provided
def ill(kappa, seed=0):
    rng = np.random.default_rng(seed)
    U, _ = np.linalg.qr(rng.normal(size=(40, 8)))
    V, _ = np.linalg.qr(rng.normal(size=(8, 8)))
    return U @ np.diag(np.logspace(0, -np.log10(kappa), 8)) @ V.T


def cgs(A):
    """Classical Gram-Schmidt."""
    raise NotImplementedError


def mgs(A):
    """Modified Gram-Schmidt."""
    raise NotImplementedError


def cgs2(A):
    """Classical Gram-Schmidt with a second pass."""
    raise NotImplementedError


def loss_of_orthogonality(Q):
    """||Q^T Q - I||."""
    raise NotImplementedError
