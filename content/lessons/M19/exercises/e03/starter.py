import numpy as np


def matmul_backward(X, W, G):
    """(dX, dW) for Y = X W."""
    raise NotImplementedError


def bias_backward(G):
    """Sum over the broadcast batch axis."""
    raise NotImplementedError


def relu_backward(Z, G):
    """Gradient through max(0, Z)."""
    raise NotImplementedError


def mse_backward(P, T):
    """Gradient of the mean squared error."""
    raise NotImplementedError
