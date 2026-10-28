import numpy as np


def target_update(d, rank, seed=0, decay=0.7):
    """A d x d update whose singular values fall geometrically, sigma_i = decay^i, for i < rank."""
    rng = np.random.default_rng(seed)
    U, _ = np.linalg.qr(rng.normal(size=(d, d)))
    V, _ = np.linalg.qr(rng.normal(size=(d, d)))
    s = np.zeros(d)
    s[:rank] = decay ** np.arange(rank)
    return (U * s) @ V.T


def error_by_rank(M, ranks):
    """Relative Frobenius error of the best rank-r approximation for each r."""
    S = np.linalg.svd(M, compute_uv=False)
    total = np.sum(S ** 2)
    return [float(np.sqrt(np.sum(S[r:] ** 2) / total)) for r in ranks]
