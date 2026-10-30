import numpy as np


def lstsq_normal(A, b):
    """Normal equations."""
    return np.linalg.solve(A.T @ A, A.T @ b)


def lstsq_qr(A, b):
    """Householder QR."""
    Q, R = np.linalg.qr(A)
    return np.linalg.solve(R, Q.T @ b)


def residual_report(A, b, x):
    """Residual size and how perpendicular it is to the columns."""
    r = b - A @ x
    return {"residual_norm": float(np.linalg.norm(r)), "max_orthogonality": float(np.max(np.abs(A.T @ r)))}
