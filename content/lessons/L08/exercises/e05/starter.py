import numpy as np


def naive_moments(x):
    """Mean and variance from one pass of sums, E[x^2] - E[x]^2, accumulated in the array's dtype."""
    raise NotImplementedError


def welford(x):
    """Mean and variance in one pass with Welford's update, in the array's dtype."""
    raise NotImplementedError


def layernorm_backward_recompute(dy, x, gamma, eps=1e-5):
    """Fused layer-norm backward that recomputes mean and 1/std from x instead of storing them.
    Return (dx, dgamma, dbeta)."""
    raise NotImplementedError
