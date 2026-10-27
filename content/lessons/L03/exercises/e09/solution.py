import numpy as np


def loss(X, W, G):
    return float(np.sum(G * (X @ W)))


def matmul_backward(X, W, G):
    """Return (dX, dW)."""
    return G @ W.T, X.T @ G
