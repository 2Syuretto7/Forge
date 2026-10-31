import numpy as np


def lora_forward(x, W, A, B, alpha):
    """y = x W^T + (alpha / r) x A^T B^T for x (n, d_in), W (d_out, d_in), A (r, d_in), B (d_out, r)."""
    raise NotImplementedError


def lora_backward(x, A, B, alpha, gy):
    """Gradients (dA, dB) of a loss whose gradient with respect to the output y is gy."""
    raise NotImplementedError


def merge(W, A, B, alpha):
    """The single weight matrix equivalent to the base weight plus the adapter."""
    raise NotImplementedError
