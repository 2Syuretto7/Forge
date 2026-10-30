import numpy as np


def gram_schmidt(A):
    """Orthonormal Q with the same column span, by modified Gram-Schmidt."""
    A = np.asarray(A, dtype=float)
    m, n = A.shape
    Q = np.zeros((m, n))
    for k in range(n):
        v = A[:, k].copy()
        for j in range(k):
            v = v - (Q[:, j] @ v) * Q[:, j]
        nv = np.linalg.norm(v)
        if nv < 1e-10 * np.linalg.norm(A[:, k]):
            raise ValueError(f"column {k} depends on earlier columns")
        Q[:, k] = v / nv
    return Q
