import numpy as np


def forward_sub(L, b):
    """Solve L y = b, L lower triangular."""
    n = len(b)
    y = np.zeros(n)
    for i in range(n):
        if L[i, i] == 0:
            raise ValueError("zero on the diagonal")
        y[i] = (b[i] - L[i, :i] @ y[:i]) / L[i, i]
    return y


def back_sub(U, c):
    """Solve U x = c, U upper triangular."""
    n = len(c)
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        if U[i, i] == 0:
            raise ValueError("zero on the diagonal")
        x[i] = (c[i] - U[i, i + 1:] @ x[i + 1:]) / U[i, i]
    return x
