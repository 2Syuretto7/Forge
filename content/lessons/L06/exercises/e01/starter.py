import numpy as np


def batchnorm_forward(x, gamma, beta, eps=1e-5):
    """Normalize each feature (column) over the batch, then scale and shift. Return (y, cache)."""
    raise NotImplementedError


def batchnorm_backward(dy, cache):
    """Return (dx, dgamma, dbeta)."""
    raise NotImplementedError
