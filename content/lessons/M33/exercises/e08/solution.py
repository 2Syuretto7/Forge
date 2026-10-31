import numpy as np


def rsvd(A, k, p=10, q=1, rng=None):
    """Randomized SVD: (U, s, Vt) of rank k."""
    rng = rng if rng is not None else np.random.default_rng(0)
    Q = np.linalg.qr(A @ rng.standard_normal((A.shape[1], k + p)))[0]
    for _ in range(q):
        Q = np.linalg.qr(A.T @ Q)[0]
        Q = np.linalg.qr(A @ Q)[0]
    Ub, s, Vt = np.linalg.svd(Q.T @ A, full_matrices=False)
    return Q @ Ub[:, :k], s[:k], Vt[:k]


def top_singular_value(A):
    """Largest singular value."""
    return float(np.linalg.svd(A, compute_uv=False)[0])


def grad_top_singular_value(A):
    """Gradient of the largest singular value: u1 v1^T."""
    U, _, Vt = np.linalg.svd(A, full_matrices=False)
    return np.outer(U[:, 0], Vt[0])
