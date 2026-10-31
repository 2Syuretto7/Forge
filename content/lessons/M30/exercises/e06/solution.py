import numpy as np


def dual_objective(alpha, X, y):
    """SVM dual objective."""
    w = X.T @ (alpha * y)
    return float(alpha.sum() - 0.5 * w @ w)


def dual_grad(alpha, X, y):
    """Gradient of the dual objective."""
    return 1 - y * (X @ (X.T @ (alpha * y)))


def coordinate_ascent(X, y, C, epochs, rng):
    """Dual coordinate ascent; returns (alpha, w)."""
    n = len(y)
    alpha = np.zeros(n)
    w = np.zeros(X.shape[1])
    sq = np.sum(X * X, axis=1)
    for _ in range(epochs):
        for i in rng.permutation(n):
            G = y[i] * (w @ X[i]) - 1
            new = min(max(alpha[i] - G / sq[i], 0.0), C)
            if new != alpha[i]:
                w += (new - alpha[i]) * y[i] * X[i]
                alpha[i] = new
    return alpha, w
