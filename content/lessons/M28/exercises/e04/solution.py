import numpy as np


def _softplus(z):
    return np.maximum(z, 0) + np.log1p(np.exp(-np.abs(z)))


def _sigmoid(z):
    e = np.exp(-np.abs(z))
    return np.where(z >= 0, 1 / (1 + e), e / (1 + e))


def logistic_loss(w, X, y):
    """Average logistic loss."""
    z = np.asarray(X, dtype=float) @ w
    return float(np.mean(_softplus(z) - y * z))


def logistic_grad(w, X, y):
    """Gradient of the average logistic loss."""
    X = np.asarray(X, dtype=float)
    return X.T @ (_sigmoid(X @ w) - y) / len(y)


def tangent_gap(f, grad, x, y_point):
    """f(y) - f(x) - grad(x) . (y - x)."""
    x, y_point = np.asarray(x, dtype=float), np.asarray(y_point, dtype=float)
    return float(f(y_point) - f(x) - grad(x) @ (y_point - x))
