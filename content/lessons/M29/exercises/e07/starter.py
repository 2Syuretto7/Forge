import numpy as np


def example_grads(X, y, w):
    """Per-example gradients of (1/2)(x^T w - y)^2."""
    raise NotImplementedError


def full_grad(X, y, w):
    """Average gradient."""
    raise NotImplementedError


def loss(X, y, w):
    """Average loss."""
    raise NotImplementedError


def minibatch_variance(X, y, w, batch, draws, rng):
    """Total variance of minibatch gradients drawn with replacement."""
    raise NotImplementedError
