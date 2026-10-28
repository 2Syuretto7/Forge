import numpy as np


def lora_forward(x, W0, A, B, alpha):
    """y = x W0^T + (alpha / r) (x A^T) B^T, with the frozen weight W0 (out, in), A (r, in) and
    B (out, r)."""
    raise NotImplementedError


def lora_backward(dy, x, W0, A, B, alpha):
    """Gradients of the loss with respect to A, B and x, given dL/dy; W0 is frozen and gets none."""
    raise NotImplementedError
