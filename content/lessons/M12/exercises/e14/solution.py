import numpy as np


# provided
def ill(kappa, seed=0):
    rng = np.random.default_rng(seed)
    U, _ = np.linalg.qr(rng.normal(size=(40, 8)))
    V, _ = np.linalg.qr(rng.normal(size=(8, 8)))
    return U @ np.diag(np.logspace(0, -np.log10(kappa), 8)) @ V.T


def cgs(A):
    """Classical Gram-Schmidt."""
    m, n = A.shape
    Q = np.zeros((m, n))
    for k in range(n):
        v = A[:, k] - Q[:, :k] @ (Q[:, :k].T @ A[:, k])
        Q[:, k] = v / np.linalg.norm(v)
    return Q


def mgs(A):
    """Modified Gram-Schmidt."""
    m, n = A.shape
    Q = np.zeros((m, n))
    for k in range(n):
        v = A[:, k].copy()
        for j in range(k):
            v -= (Q[:, j] @ v) * Q[:, j]
        Q[:, k] = v / np.linalg.norm(v)
    return Q


def cgs2(A):
    """Classical Gram-Schmidt with a second pass."""
    m, n = A.shape
    Q = np.zeros((m, n))
    for k in range(n):
        v = A[:, k] - Q[:, :k] @ (Q[:, :k].T @ A[:, k])
        v = v - Q[:, :k] @ (Q[:, :k].T @ v)
        Q[:, k] = v / np.linalg.norm(v)
    return Q


def loss_of_orthogonality(Q):
    """||Q^T Q - I||."""
    return float(np.linalg.norm(Q.T @ Q - np.eye(Q.shape[1])))
