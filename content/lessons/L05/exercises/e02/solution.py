import numpy as np


def ridge(X, y, lam):
    d = X.shape[1]
    return np.linalg.solve(X.T @ X + lam * np.eye(d), X.T @ y)


def map_objective(w, X, y, sigma2, tau2):
    r = y - X @ w
    return float(r @ r / (2 * sigma2) + w @ w / (2 * tau2))


def effective_condition(X, lam):
    return float(np.linalg.cond(X.T @ X + lam * np.eye(X.shape[1])))
