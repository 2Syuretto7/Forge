import numpy as np


# provided
def make_matrix(m, n, decay, rng):
    U = np.linalg.qr(rng.standard_normal((m, n)))[0]
    V = np.linalg.qr(rng.standard_normal((n, n)))[0]
    return (U / np.arange(1, n + 1) ** decay) @ V.T


def _rsvd(A, k, p, q, rng):
    Q = np.linalg.qr(A @ rng.standard_normal((A.shape[1], k + p)))[0]
    for _ in range(q):
        Q = np.linalg.qr(A.T @ Q)[0]
        Q = np.linalg.qr(A @ Q)[0]
    Ub, s, Vt = np.linalg.svd(Q.T @ A, full_matrices=False)
    return Q @ Ub[:, :k], s[:k], Vt[:k]


def relative_errors(A, ks, p, q, rng):
    """Relative Frobenius errors of randomized SVDs of each rank."""
    total = np.linalg.norm(A)
    out = []
    for k in ks:
        U, s, Vt = _rsvd(A, k, p, q, rng)
        out.append(float(np.linalg.norm(A - (U * s) @ Vt) / total))
    return out


def optimal_errors(s, ks):
    """Relative Frobenius errors of truncated SVDs."""
    s = np.asarray(s)
    total = np.sqrt(np.sum(s**2))
    return [float(np.sqrt(np.sum(s[k:] ** 2)) / total) for k in ks]


def matvecs(k, p, q):
    """Products of A or A^T with vectors."""
    return (k + p) * (2 * q + 2)
