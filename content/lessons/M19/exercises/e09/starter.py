import numpy as np


def loss(U, V, X):
    """Return 0.5 * ||X - U V^T||_F^2 as a float."""
    raise NotImplementedError


def grads(U, V, X):
    """Return (dU, dV), gradients of the loss."""
    raise NotImplementedError


def fit(X, k, steps, lr, seed=0):
    """Gradient descent from small random U (m, k), V (n, k). Return (U, V)."""
    raise NotImplementedError
