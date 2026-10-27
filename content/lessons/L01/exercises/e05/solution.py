import numpy as np


def lstsq_normal(A, b):
    """Return x (n,) solving the normal equations."""
    return np.linalg.solve(A.T @ A, A.T @ b)


def lstsq_qr(A, b):
    """Return x (n,) using the QR factorization of A."""
    Q, R = np.linalg.qr(A)
    return np.linalg.solve(R, Q.T @ b)


def residual_report(A, b, x):
    """Return {"residual_norm": float, "max_orthogonality": float}."""
    r = b - A @ x
    return {
        "residual_norm": float(np.linalg.norm(r)),
        "max_orthogonality": float(np.max(np.abs(A.T @ r))),
    }
