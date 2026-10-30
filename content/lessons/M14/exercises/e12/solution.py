import numpy as np


# provided
def make_update(seed=0, d=256):
    rng = np.random.default_rng(seed)
    U, _ = np.linalg.qr(rng.normal(size=(d, d)))
    V, _ = np.linalg.qr(rng.normal(size=(d, d)))
    return U @ np.diag(0.6 ** np.arange(d) + 1e-3) @ V.T


def lora_params(d_out, d_in, r):
    """Trainable numbers in a rank-r update."""
    return r * (d_out + d_in)


def best_rank_r(delta, r):
    """Factors (B, A) of the best rank-r approximation."""
    U, s, Vt = np.linalg.svd(delta)
    root = np.sqrt(s[:r])
    return U[:, :r] * root, root[:, None] * Vt[:r]


def captured(delta, r):
    """Fraction of the squared Frobenius norm kept at rank r."""
    s = np.linalg.svd(delta, compute_uv=False)
    return float(np.sum(s[:r] ** 2) / np.sum(s ** 2))
