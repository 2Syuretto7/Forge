import numpy as np


# provided
def lu(A):
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


def _perm_sign(P):
    order = list(np.argmax(P, axis=1))
    sign = 1
    for i in range(len(order)):
        while order[i] != i:
            j = order[i]
            order[i], order[j] = order[j], order[i]
            sign = -sign
    return sign


def lu_solve(P, L, U, b):
    """Solve A x = b from P A = L U."""
    pb = P @ b
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        y[i] = pb[i] - L[i, :i] @ y[:i]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
    return x


def det_from_lu(P, U):
    """det A from the factors."""
    return _perm_sign(P) * float(np.prod(np.diag(U)))


def solve_many(A, B):
    """Factor once, solve for each column of B."""
    P, L, U = lu(A)
    return np.column_stack([lu_solve(P, L, U, B[:, j]) for j in range(B.shape[1])])
