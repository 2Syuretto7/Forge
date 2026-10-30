import numpy as np


def loss(U, V, X):
    """Return 0.5 * ||X - U V^T||_F^2 as a float."""
    R = X - U @ V.T
    return float(0.5 * np.sum(R * R))


def grads(U, V, X):
    """Return (dU, dV), gradients of the loss."""
    R = X - U @ V.T
    return -R @ V, -R.T @ U


def fit(X, k, steps, lr, seed=0):
    """Gradient descent from small random U (m, k), V (n, k). Return (U, V)."""
    rng = np.random.default_rng(seed)
    m, n = X.shape
    U = 0.1 * rng.normal(size=(m, k))
    V = 0.1 * rng.normal(size=(n, k))
    for _ in range(steps):
        dU, dV = grads(U, V, X)
        U = U - lr * dU
        V = V - lr * dV
    return U, V
