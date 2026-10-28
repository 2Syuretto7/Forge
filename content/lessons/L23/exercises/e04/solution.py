import numpy as np


def probe_loss(w, b, A, y, l2=1e-3):
    """A linear probe on activations A (n, d) for binary labels y: mean logistic loss of
    sigmoid(A w + b) plus l2 / 2 |w|^2. Return (loss, dw, db)."""
    z = A @ w + b
    p = 1 / (1 + np.exp(-z))
    loss = np.mean(np.logaddexp(0, z) - y * z) + 0.5 * l2 * w @ w
    g = (p - y) / len(y)
    return float(loss), A.T @ g + l2 * w, float(g.sum())


def train_probe(A, y, steps=500, lr=1.0, l2=1e-3):
    w, b = np.zeros(A.shape[1]), 0.0
    for _ in range(steps):
        _, dw, db = probe_loss(w, b, A, y, l2)
        w -= lr * dw
        b -= lr * db
    return w, b


def probe_accuracy(w, b, A, y):
    return float(np.mean(((A @ w + b) > 0) == (y == 1)))
