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


def classify(A, b, tol=1e-10):
    """("none" | "unique" | "infinite", a solution or None)."""
    n = A.shape[1]
    R, pivots = rref(np.column_stack([A, b]), tol)
    if n in pivots:
        return "none", None
    x = np.zeros(n)
    for i, p in enumerate(pivots):
        x[p] = R[i, -1]
    return ("unique" if len(pivots) == n else "infinite"), x
