import numpy as np


def eliminate(A, b):
    """Upper triangular (U, c) by row operations, no swaps."""
    U = A.astype(float)
    c = b.astype(float)
    n = len(c)
    for k in range(n):
        if U[k, k] == 0:
            raise ValueError(f"zero pivot in column {k}")
        for i in range(k + 1, n):
            m = U[i, k] / U[k, k]
            U[i, k:] -= m * U[k, k:]
            c[i] -= m * c[k]
    return U, c


def solve_naive(A, b):
    """Elimination without pivoting, then back substitution."""
    U, c = eliminate(A, b)
    n = len(c)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (c[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
    return x
