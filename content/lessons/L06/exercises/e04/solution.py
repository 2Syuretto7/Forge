import numpy as np


def ridge_loss(w, X, y, lam):
    r = X @ w - y
    return float(np.mean(r ** 2) + lam * w @ w)


def ridge_grad(w, X, y, lam):
    n = X.shape[0]
    return 2.0 / n * X.T @ (X @ w - y) + 2.0 * lam * w


def ridge_closed_form(X, y, lam):
    n, p = X.shape
    return np.linalg.solve(X.T @ X + n * lam * np.eye(p), X.T @ y)
