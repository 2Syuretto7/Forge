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


def batch_dependence(norm, x, batch_a, batch_b):
    """Normalize example x inside two different batches (x stacked on top of batch_a, then of
    batch_b) with norm "batch" (train-mode batch norm) or "layer". Return the largest absolute
    difference between the two outputs for x."""
    raise NotImplementedError


def batch_mean_noise(B, trials=2000, seed=0):
    """Standard deviation, over trials, of the batch mean of B unit-normal values."""
    raise NotImplementedError
