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
        l = U[k + 1:, k] / U[k, k]
        L[k + 1:, k] = l
        U[k + 1:, k:] -= np.outer(l, U[k, k:])
    return perm, L, U


def _perm_sign(perm):
    order, sign = list(perm), 1
    for i in range(len(order)):
        while order[i] != i:
            j = order[i]
            order[i], order[j] = order[j], order[i]
            sign = -sign
    return sign


def logabsdet(A):
    """(sign, log |det A|)."""
    perm, L, U = lu(A)
    d = np.diag(U)
    if np.any(d == 0):
        return 0, -np.inf
    sign = _perm_sign(perm) * int(np.prod(np.sign(d)))
    return sign, float(np.sum(np.log(np.abs(d))))


def naive_det(A):
    """Product of the pivots, with the permutation's sign."""
    perm, L, U = lu(A)
    with np.errstate(over="ignore"):
        return _perm_sign(perm) * float(np.prod(np.diag(U)))
