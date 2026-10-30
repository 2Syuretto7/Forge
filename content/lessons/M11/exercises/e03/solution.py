import numpy as np


def lu(A):
    """(P, L, U) with P A = L U, partial pivoting."""
    n = A.shape[0]
    U = A.astype(float)
    L = np.eye(n)
    perm = list(range(n))
    for k in range(n - 1):
        p = k + int(np.argmax(np.abs(U[k:, k])))
        if U[p, k] == 0:
            continue
        if p != k:
            U[[k, p]] = U[[p, k]]
            L[[k, p], :k] = L[[p, k], :k]
            perm[k], perm[p] = perm[p], perm[k]
        for i in range(k + 1, n):
            L[i, k] = U[i, k] / U[k, k]
            U[i, k:] -= L[i, k] * U[k, k:]
            U[i, k] = 0.0
    return np.eye(n)[perm], L, U
