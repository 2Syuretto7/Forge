import numpy as np


def naive_moments(x):
    """Mean and variance from one pass of sums, E[x^2] - E[x]^2, accumulated in the array's dtype."""
    n = x.dtype.type(x.size)
    s = x.sum(dtype=x.dtype)
    s2 = (x * x).sum(dtype=x.dtype)
    mean = s / n
    return mean, s2 / n - mean * mean


def welford(x):
    """Mean and variance in one pass with Welford's update, in the array's dtype."""
    mean = x.dtype.type(0)
    m2 = x.dtype.type(0)
    for i, v in enumerate(x, start=1):
        d = v - mean
        mean = mean + d / x.dtype.type(i)
        m2 = m2 + d * (v - mean)
    return mean, m2 / x.dtype.type(x.size)


def layernorm_backward_recompute(dy, x, gamma, eps=1e-5):
    """Fused layer-norm backward that recomputes mean and 1/std from x instead of storing them.
    Return (dx, dgamma, dbeta)."""
    mu = x.mean(axis=1, keepdims=True)
    r = 1.0 / np.sqrt(x.var(axis=1, keepdims=True) + eps)
    xh = (x - mu) * r
    g = dy * gamma
    d = x.shape[1]
    dx = r / d * (d * g - g.sum(axis=1, keepdims=True) - xh * (g * xh).sum(axis=1, keepdims=True))
    return dx, (dy * xh).sum(axis=0), dy.sum(axis=0)
