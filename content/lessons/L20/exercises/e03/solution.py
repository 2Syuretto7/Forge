import numpy as np


def lora_forward(x, W0, A, B, alpha):
    """y = x W0^T + (alpha / r) (x A^T) B^T, with the frozen weight W0 (out, in), A (r, in) and
    B (out, r)."""
    s = alpha / A.shape[0]
    return x @ W0.T + s * (x @ A.T) @ B.T


def lora_backward(dy, x, W0, A, B, alpha):
    """Gradients of the loss with respect to A, B and x, given dL/dy; W0 is frozen and gets none."""
    s = alpha / A.shape[0]
    dB = s * dy.T @ (x @ A.T)
    dA = s * (dy @ B).T @ x
    dx = dy @ W0 + s * (dy @ B) @ A
    return dA, dB, dx
