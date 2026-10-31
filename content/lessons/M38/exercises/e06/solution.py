import numpy as np


def lora_params(k, d, r):
    """Trainable parameters of a rank-r LoRA update."""
    return r * (k + d)


def full_params(k, d):
    """Parameters of the full matrix."""
    return k * d


def fraction(k, d, r):
    """LoRA parameters as a fraction of the full matrix."""
    return lora_params(k, d, r) / full_params(k, d)


def merged(W0, B, A):
    """W0 + B A."""
    return np.asarray(W0) + np.asarray(B) @ np.asarray(A)


def rank_of(M, tol=1e-9):
    """Numerical rank."""
    s = np.linalg.svd(np.asarray(M), compute_uv=False)
    return int(np.sum(s > tol * s[0])) if s[0] > 0 else 0
