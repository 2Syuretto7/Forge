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


def layernorm_forward(x, gamma, beta, eps=1e-5):
    """Normalize each example (row) over its features, then scale and shift. Return (y, cache)."""
    mu = x.mean(axis=1, keepdims=True)
    var = x.var(axis=1, keepdims=True)
    r = 1.0 / np.sqrt(var + eps)
    xh = (x - mu) * r
    return gamma * xh + beta, (xh, r, gamma)


def layernorm_backward(dy, cache):
    """Return (dx, dgamma, dbeta)."""
    xh, r, gamma = cache
    d = dy.shape[1]
    dgamma = (dy * xh).sum(axis=0)
    dbeta = dy.sum(axis=0)
    dxh = dy * gamma
    dx = r / d * (d * dxh - dxh.sum(axis=1, keepdims=True) - xh * (dxh * xh).sum(axis=1, keepdims=True))
    return dx, dgamma, dbeta


def batch_of_one(x, gamma, beta):
    """Train-mode batch norm on a batch holding the single row x, and the gradient it passes back
    for an upstream gradient of ones. Return (y, dx)."""
    raise NotImplementedError


def layernorm_of_one(x, gamma, beta):
    """The same single row through layer norm, and its gradient for an upstream gradient that
    weights the features 1, 2, ..., d. Return (y, dx)."""
    raise NotImplementedError
