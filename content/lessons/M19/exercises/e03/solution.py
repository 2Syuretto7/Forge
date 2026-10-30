import numpy as np


def matmul_backward(X, W, G):
    """(dX, dW) for Y = X W."""
    return G @ W.T, X.T @ G


def bias_backward(G):
    """Sum over the broadcast batch axis."""
    return G.sum(axis=0)


def relu_backward(Z, G):
    """Gradient through max(0, Z)."""
    return (Z > 0) * G


def mse_backward(P, T):
    """Gradient of the mean squared error."""
    return 2 * (P - T) / P.size
