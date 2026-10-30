import numpy as np


def rank_k_approx(A, k):
    """Return the best rank-k approximation of A (same shape as A)."""
    U, s, Vt = np.linalg.svd(A, full_matrices=False)
    return (U[:, :k] * s[:k]) @ Vt[:k]


def eckart_young_error(s, k):
    """s: all singular values, descending. Return ||A - A_k||_F."""
    s = np.asarray(s, dtype=float)
    return float(np.sqrt(np.sum(s[k:] ** 2)))


def compression_ratio(m, n, k):
    """Return (m * n) / (k * (m + n + 1))."""
    return m * n / (k * (m + n + 1))


def smallest_k(A, rel_tol):
    """Smallest k >= 0 with ||A - A_k||_F / ||A||_F <= rel_tol."""
    s = np.linalg.svd(A, compute_uv=False)
    total = np.sum(s ** 2)
    for k in range(len(s) + 1):
        if np.sum(s[k:] ** 2) <= rel_tol ** 2 * total:
            return k
    return len(s)
