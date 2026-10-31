import numpy as np


def primal_objective(w, X, y, C):
    """Soft-margin SVM objective."""
    return float(0.5 * w @ w + C * np.sum(np.maximum(0, 1 - y * (X @ w))))


def margin_violations(w, X, y):
    """Points inside the margin or misclassified."""
    return y * (X @ w) < 1


def subgradient(w, X, y, C):
    """A subgradient of the primal objective."""
    v = margin_violations(w, X, y)
    return w - C * (y[v] @ X[v])


def subgradient_descent(X, y, C, iters):
    """Best iterate of the subgradient method with steps 1/(k+1)."""
    w = np.zeros(X.shape[1])
    best, fbest = w.copy(), primal_objective(w, X, y, C)
    for k in range(iters):
        w = w - subgradient(w, X, y, C) / (k + 1)
        f = primal_objective(w, X, y, C)
        if f < fbest:
            best, fbest = w.copy(), f
    return best
