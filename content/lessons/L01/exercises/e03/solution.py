import numpy as np


def gram_schmidt(A):
    """A: (m, n), m >= n, independent columns. Return Q: (m, n) orthonormal columns.

    Raise ValueError if a column depends on the previous ones.
    """
    A = np.asarray(A, dtype=float)
    m, n = A.shape
    Q = np.zeros((m, n))
    for k in range(n):
        v = A[:, k].copy()
        for j in range(k):
            v = v - (Q[:, j] @ v) * Q[:, j]
        nv = np.linalg.norm(v)
        if nv < 1e-10 * np.linalg.norm(A[:, k]):
            raise ValueError(f"column {k} is linearly dependent on earlier columns")
        Q[:, k] = v / nv
    return Q
