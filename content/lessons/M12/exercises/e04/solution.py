import numpy as np


def qr(A):
    """A = QR by modified Gram-Schmidt, diag(R) > 0."""
    A = np.asarray(A, dtype=float)
    m, n = A.shape
    Q = np.zeros((m, n))
    R = np.zeros((n, n))
    for k in range(n):
        v = A[:, k].copy()
        for j in range(k):
            R[j, k] = Q[:, j] @ v
            v -= R[j, k] * Q[:, j]
        R[k, k] = np.linalg.norm(v)
        Q[:, k] = v / R[k, k]
    return Q, R


def back_substitute(R, y):
    """Solve R x = y, R upper triangular."""
    n = R.shape[0]
    x = np.zeros(n)
    for i in range(n - 1, -1, -1):
        x[i] = (y[i] - R[i, i + 1:] @ x[i + 1:]) / R[i, i]
    return x


def lstsq_qr(A, b):
    """Least squares through A = QR."""
    Q, R = qr(A)
    return back_substitute(R, Q.T @ b)
