import numpy as np


def is_psd(C, tol=1e-10):
    """Whether C has no eigenvalue below -tol."""
    return bool(np.linalg.eigvalsh(np.asarray(C, dtype=float))[0] >= -tol)


def negative_variance_direction(C):
    """Unit vector minimizing a^T C a."""
    w, V = np.linalg.eigh(np.asarray(C, dtype=float))
    return V[:, 0]


def nearest_correlation(C, eps=1e-6):
    """Clip eigenvalues and restore a unit diagonal."""
    w, V = np.linalg.eigh(np.asarray(C, dtype=float))
    M = (V * np.maximum(w, eps)) @ V.T
    D = 1 / np.sqrt(np.diag(M))
    return M * np.outer(D, D)
