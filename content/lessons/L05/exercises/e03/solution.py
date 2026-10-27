import numpy as np


def mse(w, X, y):
    r = X @ w - y
    return float(np.mean(r ** 2))


def mse_grad(w, X, y):
    return 2.0 / X.shape[0] * X.T @ (X @ w - y)


def gd(X, y, lr, steps):
    w = np.zeros(X.shape[1])
    losses = []
    for _ in range(steps):
        losses.append(mse(w, X, y))
        w = w - lr * mse_grad(w, X, y)
    return w, losses


def max_stable_lr(X):
    n = X.shape[0]
    return float(2.0 / np.linalg.eigvalsh(2.0 / n * X.T @ X).max())
