import numpy as np


def ill_matrix(kappa, seed=0):
    """40 x 6 matrix with singular values from 1 to 1/kappa."""
    rng = np.random.default_rng(seed)
    U, _ = np.linalg.qr(rng.normal(size=(40, 6)))
    V, _ = np.linalg.qr(rng.normal(size=(6, 6)))
    return U @ np.diag(np.logspace(0, -np.log10(kappa), 6)) @ V.T


def smallest_two_ways(A):
    """(smallest singular value from the SVD, from eig of A^T A)."""
    s = np.linalg.svd(A, compute_uv=False)
    w = np.linalg.eigvalsh(A.T @ A)
    return float(s[-1]), float(np.sqrt(max(w[0], 0.0)))


def normal_vs_qr(A, x_true):
    """Relative errors of the normal equations and QR."""
    b = A @ x_true
    xn = np.linalg.solve(A.T @ A, A.T @ b)
    Q, R = np.linalg.qr(A)
    xq = np.linalg.solve(R, Q.T @ b)
    nt = np.linalg.norm(x_true)
    return {"normal": float(np.linalg.norm(xn - x_true) / nt), "qr": float(np.linalg.norm(xq - x_true) / nt)}
