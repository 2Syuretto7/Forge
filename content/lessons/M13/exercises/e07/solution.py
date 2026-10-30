import numpy as np


def transition_matrix(C):
    """Columns of counts normalized to sum to 1."""
    C = np.asarray(C, dtype=float)
    return C / C.sum(axis=0, keepdims=True)


def stationary_power(P, tol=1e-12, max_iter=100000):
    """Iterate p <- P p from the uniform distribution."""
    n = P.shape[0]
    p = np.full(n, 1.0 / n)
    for _ in range(max_iter):
        q = P @ p
        if np.abs(q - p).sum() < tol:
            return q
        p = q
    return p


def stationary_eig(P):
    """Eigenvector of the eigenvalue nearest 1, summing to 1."""
    lam, V = np.linalg.eig(P)
    v = np.real(V[:, np.argmin(np.abs(lam - 1))])
    return v / v.sum()
