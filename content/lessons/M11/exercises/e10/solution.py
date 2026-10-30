import time

import numpy as np


def lu_fast(A):
    """(perm, L, U) with A[perm] = L U, one outer-product update per pivot."""
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


def solve_fast(A, b):
    """Solve A x = b with lu_fast."""
    perm, L, U = lu_fast(A)
    n = len(b)
    pb = b[perm]
    y = np.zeros(n)
    for i in range(n):
        y[i] = pb[i] - L[i, :i] @ y[:i]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
    return x


def compare(n, seed=0):
    """Times and relative residuals of solve_fast and np.linalg.solve."""
    rng = np.random.default_rng(seed)
    A, b = rng.normal(size=(n, n)), rng.normal(size=n)
    res = lambda x: float(np.linalg.norm(A @ x - b) / (np.linalg.norm(A) * np.linalg.norm(x)))
    t0 = time.perf_counter()
    x1 = solve_fast(A, b)
    t1 = time.perf_counter()
    x2 = np.linalg.solve(A, b)
    t2 = time.perf_counter()
    return {"mine_s": t1 - t0, "numpy_s": t2 - t1, "mine_res": res(x1), "numpy_res": res(x2)}
