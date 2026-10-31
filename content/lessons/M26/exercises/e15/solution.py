import numpy as np


def _eliminate(A, b, pivot):
    A = np.array(A, dtype=float)
    b = np.array(b, dtype=float)
    n = len(b)
    big = np.abs(A).max()
    for k in range(n - 1):
        if pivot:
            p = k + int(np.argmax(np.abs(A[k:, k])))
            A[[k, p]] = A[[p, k]]
            b[[k, p]] = b[[p, k]]
        for i in range(k + 1, n):
            m = A[i, k] / A[k, k]
            A[i, k:] -= m * A[k, k:]
            b[i] -= m * b[k]
        big = max(big, np.abs(A).max())
    return A, b, big


def _back(U, c):
    n = len(c)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (c[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
    return x


def solve_no_pivot(A, b):
    """Gaussian elimination without pivoting."""
    U, c, _ = _eliminate(A, b, False)
    return _back(U, c)


def solve_partial_pivot(A, b):
    """Gaussian elimination with partial pivoting."""
    U, c, _ = _eliminate(A, b, True)
    return _back(U, c)


def growth_factor(A, pivot):
    """Largest entry during elimination over the largest entry of A."""
    _, _, big = _eliminate(A, np.zeros(len(A)), pivot)
    return float(big / np.abs(np.asarray(A, dtype=float)).max())
