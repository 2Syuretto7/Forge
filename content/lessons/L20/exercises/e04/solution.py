import numpy as np


def lora_forward(x, W, A, B, alpha):
    """y = x W^T + (alpha / r) x A^T B^T for x (n, d_in), W (d_out, d_in), A (r, d_in), B (d_out, r)."""
    return x @ W.T + (alpha / A.shape[0]) * (x @ A.T) @ B.T


def lora_backward(x, A, B, alpha, gy):
    """Gradients (dA, dB) of a loss whose gradient with respect to the output y is gy."""
    s = alpha / A.shape[0]
    dB = s * gy.T @ (x @ A.T)
    dA = s * (gy @ B).T @ x
    return dA, dB


def merge(W, A, B, alpha):
    """The single weight matrix equivalent to the base weight plus the adapter."""
    return W + (alpha / A.shape[0]) * B @ A
