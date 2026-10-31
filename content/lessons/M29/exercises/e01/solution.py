import numpy as np


def _softplus(z):
    return np.maximum(z, 0) + np.log1p(np.exp(-np.abs(z)))


def _sigmoid(z):
    e = np.exp(-np.abs(z))
    return np.where(z >= 0, 1 / (1 + e), e / (1 + e))


def loss(w, X, y):
    """Average logistic loss."""
    z = X @ w
    return float(np.mean(_softplus(z) - y * z))


def grad(w, X, y):
    """Gradient of the average logistic loss."""
    return X.T @ (_sigmoid(X @ w) - y) / len(y)


def gd(X, y, w0, step, iters):
    """Iterates of gradient descent."""
    w = np.array(w0, dtype=float)
    out = [w.copy()]
    for _ in range(iters):
        w = w - step * grad(w, X, y)
        out.append(w.copy())
    return out


def descent_lemma_holds(X, y, w0, iters):
    """Whether every step of size 1/L decreases f by at least |grad|^2 / (2L)."""
    L = np.linalg.eigvalsh(X.T @ X)[-1] / (4 * len(y))
    ws = gd(X, y, w0, 1 / L, iters)
    for a, b in zip(ws, ws[1:]):
        g = grad(a, X, y)
        if loss(b, X, y) > loss(a, X, y) - (g @ g) / (2 * L) + 1e-12:
            return False
    return True
