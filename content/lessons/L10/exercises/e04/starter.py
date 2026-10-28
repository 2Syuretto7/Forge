import numpy as np


def rmsnorm_forward(x, gamma, eps=1e-6):
    """Divide each row by its root mean square (no centering), then scale. Return (y, cache)."""
    raise NotImplementedError


def rmsnorm_backward(dy, cache):
    """Return (dx, dgamma)."""
    raise NotImplementedError
