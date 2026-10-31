import numpy as np


# provided
def make_matrix(m, n, decay, rng):
    U = np.linalg.qr(rng.standard_normal((m, n)))[0]
    V = np.linalg.qr(rng.standard_normal((n, n)))[0]
    return (U / np.arange(1, n + 1) ** decay) @ V.T


def _approx(A, k, p, q, rng):
    Q = np.linalg.qr(A @ rng.standard_normal((A.shape[1], k + p)))[0]
    for _ in range(q):
        Q = np.linalg.qr(A.T @ Q)[0]
        Q = np.linalg.qr(A @ Q)[0]
    Ub, s, Vt = np.linalg.svd(Q.T @ A, full_matrices=False)
    return (Q @ Ub[:, :k] * s[:k]) @ Vt[:k]


def rsvd_error_ratio(A, s, k, p, q, rng):
    """Frobenius error relative to the optimum."""
    return float(np.linalg.norm(A - _approx(A, k, p, q, rng)) / np.sqrt(np.sum(np.asarray(s)[k:] ** 2)))


def spectral_error_ratio(A, s, k, p, q, rng):
    """Spectral error relative to sigma_{k+1}."""
    return float(np.linalg.norm(A - _approx(A, k, p, q, rng), 2) / s[k])
