import numpy as np
import math


C = math.sqrt(2.0 / math.pi)


def gelu(x):
    """The tanh approximation used by GPT-2: 0.5 x (1 + tanh(c (x + 0.044715 x^3)))."""
    return 0.5 * x * (1.0 + np.tanh(C * (x + 0.044715 * x ** 3)))


def gelu_grad(x):
    u = C * (x + 0.044715 * x ** 3)
    t = np.tanh(u)
    return 0.5 * (1.0 + t) + 0.5 * x * (1.0 - t * t) * C * (1.0 + 3 * 0.044715 * x * x)


def mlp_forward(x, W1, W2, store=True):
    """y = gelu(x W1) W2. With store=True keep (x, h, a) for backward; with store=False keep only x
    and recompute the rest in backward. Return (y, cache)."""
    raise NotImplementedError


def mlp_backward(dy, cache, W1, W2):
    """Return (dx, dW1, dW2), recomputing h and a if they were not stored."""
    raise NotImplementedError


def cache_floats(cache):
    return sum(c.size for c in cache)
