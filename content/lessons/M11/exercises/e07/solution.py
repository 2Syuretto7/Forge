import numpy as np


# provided
def rref(A, tol=1e-10):
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


def null_space(A, tol=1e-10):
    """Columns form a basis of {x : A x = 0}."""
    R, pivots = rref(A, tol)
    n = R.shape[1]
    free = [j for j in range(n) if j not in pivots]
    N = np.zeros((n, len(free)))
    for k, f in enumerate(free):
        N[f, k] = 1.0
        for i, p in enumerate(pivots):
            N[p, k] = -R[i, f]
    return N
