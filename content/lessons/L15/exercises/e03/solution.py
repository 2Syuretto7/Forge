import numpy as np


def layer_norm(x, eps=1e-5):
    """Normalize each row of x to zero mean and unit variance (no gain or bias). Return
    (y, cache)."""
    mu = x.mean(axis=-1, keepdims=True)
    var = x.var(axis=-1, keepdims=True)
    inv = 1 / np.sqrt(var + eps)
    y = (x - mu) * inv
    return y, (y, inv)


def layer_norm_backward(dy, cache):
    """The gradient with respect to x, given dL/dy."""
    y, inv = cache
    n = y.shape[-1]
    return inv * (dy - dy.mean(axis=-1, keepdims=True) - y * (dy * y).mean(axis=-1, keepdims=True))


def max_attention_logit(q, k, qk_norm):
    """The largest |q_i . k_j| / sqrt(d) over all pairs, with q and k (rows) layer-normalized first
    if qk_norm."""
    if qk_norm:
        q, k = layer_norm(q)[0], layer_norm(k)[0]
    return float(np.abs(q @ k.T).max() / np.sqrt(q.shape[1]))
