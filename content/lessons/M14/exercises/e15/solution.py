import numpy as np


def hilbert(n, dtype=np.float64):
    """Return the n x n Hilbert matrix with entries 1 / (i + j + 1)."""
    i = np.arange(n)
    return (1.0 / (i[:, None] + i[None, :] + 1.0)).astype(dtype)


def gauss_solve(A, b):
    """Gaussian elimination with partial pivoting in A's dtype. Return x."""
    A = np.array(A, copy=True)
    b = np.array(b, dtype=A.dtype, copy=True)
    n = A.shape[0]
    for k in range(n - 1):
        p = k + int(np.argmax(np.abs(A[k:, k])))
        if p != k:
            A[[k, p]] = A[[p, k]]
            b[[k, p]] = b[[p, k]]
        for i in range(k + 1, n):
            f = A[i, k] / A[k, k]
            A[i, k:] = A[i, k:] - f * A[k, k:]
            b[i] = b[i] - f * b[k]
    x = np.zeros(n, dtype=A.dtype)
    for i in range(n - 1, -1, -1):
        x[i] = (b[i] - A[i, i + 1:] @ x[i + 1:]) / A[i, i]
    return x


def hilbert_error(n, dtype):
    """Relative error of solving H x = H @ ones in the given dtype."""
    H = hilbert(n, dtype)
    ones = np.ones(n, dtype=dtype)
    x = gauss_solve(H, H @ ones)
    x = x.astype(np.float64)
    return float(np.linalg.norm(x - 1.0) / np.sqrt(n))
