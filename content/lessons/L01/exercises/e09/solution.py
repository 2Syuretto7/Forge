import numpy as np


def svd_via_eig(A):
    """A: (m, n). Return U (m, r), s (r,) descending, Vt (r, n) with A = U diag(s) Vt."""
    A = np.asarray(A, dtype=float)
    w, V = np.linalg.eigh(A.T @ A)
    order = np.argsort(w)[::-1]
    w = np.clip(w[order], 0.0, None)
    V = V[:, order]
    s = np.sqrt(w)
    if s[0] == 0:
        return np.zeros((A.shape[0], 0)), np.zeros(0), np.zeros((0, A.shape[1]))
    r = int(np.sum(w > 1e-12 * w[0]))
    s = s[:r]
    V = V[:, :r]
    U = (A @ V) / s
    return U, s, V.T
