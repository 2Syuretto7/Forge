import numpy as np


def hessian_condition(X):
    return float(np.linalg.cond(2.0 / X.shape[0] * X.T @ X))


def steps_to_converge(X, y, tol=1e-3, max_steps=20000):
    n = X.shape[0]
    H = 2.0 / n * X.T @ X
    lr = 0.9 * 2.0 / np.linalg.eigvalsh(H).max()
    w_star = np.linalg.lstsq(X, y, rcond=None)[0]
    w = np.zeros(X.shape[1])
    for k in range(max_steps):
        if np.linalg.norm(w - w_star) <= tol * np.linalg.norm(w_star):
            return k
        w = w - lr * (2.0 / n * X.T @ (X @ w - y))
    return max_steps


def standardize(X):
    return (X - X.mean(axis=0)) / X.std(axis=0)
