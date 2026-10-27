import numpy as np


def df_svd(X, lam):
    s2 = np.linalg.svd(X, compute_uv=False) ** 2
    return float(np.sum(s2 / (s2 + lam)))


def df_trace(X, lam):
    p = X.shape[1]
    return float(np.trace(X @ np.linalg.solve(X.T @ X + lam * np.eye(p), X.T)))


def ddf_dlam(X, lam):
    s2 = np.linalg.svd(X, compute_uv=False) ** 2
    return float(-np.sum(s2 / (s2 + lam) ** 2))
