import numpy as np


def rref(A, tol=1e-10):
    """(reduced row echelon form, pivot columns)."""
    R = np.array(A, dtype=float)
    m, n = R.shape
    pivots = []
    r = 0
    for j in range(n):
        if r == m:
            break
        p = r + int(np.argmax(np.abs(R[r:, j])))
        if abs(R[p, j]) <= tol:
            continue
        R[[r, p]] = R[[p, r]]
        R[r] /= R[r, j]
        for i in range(m):
            if i != r:
                R[i] -= R[i, j] * R[r]
        pivots.append(j)
        r += 1
    R[np.abs(R) < tol] = 0.0
    return R, pivots
