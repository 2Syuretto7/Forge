import numpy as np


# provided
def make_embeddings(n, d, seed=0):
    rng = np.random.default_rng(seed)
    Q, _ = np.linalg.qr(rng.normal(size=(d, d)))
    scale = np.arange(1, d + 1) ** -0.6
    return (rng.normal(size=(n, d)) * scale) @ Q.T + rng.normal(size=d)


def top_k_svd(X, k):
    """Top k singular values and right singular vectors of the centred data."""
    Xc = X - X.mean(axis=0)
    w, V = np.linalg.eigh(Xc.T @ Xc)
    order = np.argsort(w)[::-1][:k]
    return np.sqrt(np.clip(w[order], 0, None)), V[:, order].T


def explained(s_all):
    """Cumulative fraction of variance."""
    v = np.asarray(s_all) ** 2
    return np.cumsum(v) / v.sum()


def rank_for(s_all, fraction):
    """Smallest k reaching the fraction."""
    return int(np.argmax(explained(s_all) >= fraction - 1e-12)) + 1


def recon_error(X, Vt_k):
    """Relative Frobenius error of the reconstruction from the components."""
    Xc = X - X.mean(axis=0)
    return float(np.linalg.norm(Xc - Xc @ Vt_k.T @ Vt_k) / np.linalg.norm(Xc))
