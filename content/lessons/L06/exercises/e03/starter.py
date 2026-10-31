import numpy as np


def layernorm_forward(x, gamma, beta, eps=1e-5):
    """Normalize each example (row) over its features, then scale and shift. Return (y, cache)."""
    raise NotImplementedError


def layernorm_backward(dy, cache):
    """Return (dx, dgamma, dbeta)."""
    raise NotImplementedError
