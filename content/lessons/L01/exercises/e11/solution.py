import numpy as np


def _sig(a):
    return 0.5 * (1.0 + np.tanh(0.5 * a))


def train_norms(X, y, lr=1.0, steps=20000, l2=0.0, every=1000):
    w = np.zeros(X.shape[1])
    n = X.shape[0]
    norms = []
    for t in range(1, steps + 1):
        w = w - lr * (X.T @ (_sig(X @ w) - y) / n + l2 * w)
        if t % every == 0:
            norms.append(float(np.linalg.norm(w)))
    return norms


def train_confidence(X, y, w):
    """Return (min, max) probability assigned to the correct training label."""
    s = _sig(X @ w)
    p = np.where(y == 1, s, 1 - s)
    return float(p.min()), float(p.max())
