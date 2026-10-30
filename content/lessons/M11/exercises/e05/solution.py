import numpy as np


def rank(A, tol=None):
    """Numerical rank by elimination with complete pivoting."""
    U = np.array(A, dtype=float)
    m, n = U.shape
    big = np.max(np.abs(U)) if U.size else 0.0
    if big == 0:
        return 0
    if tol is None:
        tol = max(m, n) * 1e-12 * big
    r = 0
    for k in range(min(m, n)):
        block = np.abs(U[k:, k:])
        i, j = np.unravel_index(np.argmax(block), block.shape)
        if block[i, j] <= tol:
            break
        i, j = i + k, j + k
        U[[k, i]] = U[[i, k]]
        U[:, [k, j]] = U[:, [j, k]]
        U[k + 1:, k:] -= np.outer(U[k + 1:, k] / U[k, k], U[k, k:])
        r += 1
    return r
