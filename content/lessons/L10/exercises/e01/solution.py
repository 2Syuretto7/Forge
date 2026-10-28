import numpy as np


def batchnorm_forward(x, gamma, beta, eps=1e-5):
    """Normalize each feature (column) over the batch, then scale and shift. Return (y, cache)."""
    mu = x.mean(axis=0)
    var = x.var(axis=0)
    r = 1.0 / np.sqrt(var + eps)
    xh = (x - mu) * r
    return gamma * xh + beta, (xh, r, gamma)


def batchnorm_backward(dy, cache):
    """Return (dx, dgamma, dbeta)."""
    xh, r, gamma = cache
    n = dy.shape[0]
    dgamma = (dy * xh).sum(axis=0)
    dbeta = dy.sum(axis=0)
    dxh = dy * gamma
    dx = r / n * (n * dxh - dxh.sum(axis=0) - xh * (dxh * xh).sum(axis=0))
    return dx, dgamma, dbeta
