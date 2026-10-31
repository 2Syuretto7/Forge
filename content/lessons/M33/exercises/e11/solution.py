import numpy as np


def ridge_loss(w, X, y, lam):
    """Half squared error plus half lambda times the squared norm."""
    r = X @ w - y
    return 0.5 * r @ r + 0.5 * lam * w @ w


def grad_ridge_loss(w, X, y, lam):
    """Gradient of ridge_loss."""
    return X.T @ (X @ w - y) + lam * w


def ridge_cg(X, y, lam, tol=1e-10):
    """Matrix-free CG on the ridge normal equations: (w, products)."""
    b = X.T @ y
    w = np.zeros(X.shape[1])
    r = b.copy()
    p = r.copy()
    rr = r @ r
    target = tol * np.sqrt(rr)
    count = 0
    while np.sqrt(rr) > target and count < 10 * len(b):
        Ap = X.T @ (X @ p) + lam * p
        count += 1
        a = rr / (p @ Ap)
        w += a * p
        r -= a * Ap
        new = r @ r
        p = r + (new / rr) * p
        rr = new
    return w, count


def ridge_direct(X, y, lam):
    """Ridge solution from the formed normal equations."""
    return np.linalg.solve(X.T @ X + lam * np.eye(X.shape[1]), X.T @ y)
