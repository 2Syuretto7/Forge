import numpy as np


def rmsnorm_forward(x, gamma, eps=1e-6):
    """Divide each row by its root mean square (no centering), then scale. Return (y, cache)."""
    r = np.sqrt((x * x).mean(axis=1, keepdims=True) + eps)
    return gamma * x / r, (x, r, gamma)


def rmsnorm_backward(dy, cache):
    """Return (dx, dgamma)."""
    x, r, gamma = cache
    d = x.shape[1]
    dgamma = (dy * x / r).sum(axis=0)
    gdy = dy * gamma
    dx = gdy / r - x * (gdy * x).sum(axis=1, keepdims=True) / (d * r ** 3)
    return dx, dgamma
