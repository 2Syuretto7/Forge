import numpy as np


# provided
def make_embeddings(n, d, seed=0):
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.normal(size=(d, d)))
    scale = np.arange(1, d + 1) ** -0.6
    return (rng.normal(size=(n, d)) * scale) @ Q.T + rng.normal(size=d)


def top_k_svd(X, k):
    """Top k singular values and right singular vectors of the centred data."""
    raise NotImplementedError


def explained(s_all):
    """Cumulative fraction of variance."""
    raise NotImplementedError


def rank_for(s_all, fraction):
    """Smallest k reaching the fraction."""
    raise NotImplementedError


def recon_error(X, Vt_k):
    """Relative Frobenius error of the reconstruction from the components."""
    raise NotImplementedError
