import numpy as np


def underflow_fraction(grads, scale=1.0):
    """Fraction of the nonzero float32 gradients that become exactly 0 when (grads * scale) is cast to
    float16."""
    raise NotImplementedError


def scaled_loss_and_grad(w, X, y, scale):
    """Loss scaling: return (scale * L, scale * dL/dw) for the least-squares loss
    L = mean((X w - y)^2) / 2. The optimizer divides by scale before using the gradient."""
    raise NotImplementedError
