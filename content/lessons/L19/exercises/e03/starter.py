import numpy as np


def layer_norm(x, eps=1e-5):
    """Normalize each row of x to zero mean and unit variance (no gain or bias). Return
    (y, cache)."""
    raise NotImplementedError


def layer_norm_backward(dy, cache):
    """The gradient with respect to x, given dL/dy."""
    raise NotImplementedError


def max_attention_logit(q, k, qk_norm):
    """The largest |q_i . k_j| / sqrt(d) over all pairs, with q and k (rows) layer-normalized first
    if qk_norm."""
    raise NotImplementedError
