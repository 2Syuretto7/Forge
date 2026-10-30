import numpy as np


def spectral_norm(A):
    """Largest singular value."""
    return float(np.linalg.svd(A, compute_uv=False)[0])


def frobenius_from_s(A):
    """sqrt of the sum of squared singular values."""
    s = np.linalg.svd(A, compute_uv=False)
    return float(np.sqrt(np.sum(s * s)))


def stretch_samples(A, k=2000, seed=0):
    """Largest |A x| over k random unit vectors."""
    X = np.random.default_rng(seed).normal(size=(A.shape[1], k))
    X /= np.linalg.norm(X, axis=0)
    return float(np.max(np.linalg.norm(A @ X, axis=0)))
