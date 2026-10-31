import numpy as np


def adam(grad, x0, lr, iters, b1=0.9, b2=0.999, eps=1e-8, bias_correction=True):
    """Iterates of Adam."""
    raise NotImplementedError


def adam_moments(gs, b1=0.9, b2=0.999):
    """Bias-corrected first and second moments of a gradient sequence."""
    raise NotImplementedError
