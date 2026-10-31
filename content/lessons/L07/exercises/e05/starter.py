import numpy as np
import math


C = math.sqrt(2.0 / math.pi)


def gelu(x):
    """The tanh approximation used by GPT-2: 0.5 x (1 + tanh(c (x + 0.044715 x^3)))."""
    return 0.5 * x * (1.0 + np.tanh(C * (x + 0.044715 * x ** 3)))


def gelu_grad(x):
    """d gelu / dx."""
    raise NotImplementedError


def bias_gelu_forward(x, b):
    """y = gelu(x + b) in one pass; return (y, cache)."""
    raise NotImplementedError


def bias_gelu_backward(dy, cache):
    """Return (dx, db)."""
    raise NotImplementedError


def traffic(n, bytes_per=2, fused=True):
    """Bytes moved for x + b followed by gelu on n elements (the bias vector is negligible).
    Unfused: the add reads x and writes z, the GELU reads z and writes y. Fused: read x, write y."""
    raise NotImplementedError
