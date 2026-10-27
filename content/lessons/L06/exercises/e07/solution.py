import numpy as np


def min_norm(X, y):
    return X.T @ np.linalg.solve(X @ X.T, y)


def mse(w, X, y):
    r = X @ w - y
    return float(np.mean(r ** 2))


def mse_grad(w, X, y):
    return 2.0 / X.shape[0] * X.T @ (X @ w - y)


def gd_from_zero(X, y, lr, steps):
    w = np.zeros(X.shape[1])
    for _ in range(steps):
        w = w - lr * mse_grad(w, X, y)
    return w
