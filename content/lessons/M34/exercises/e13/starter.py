import numpy as np


def softmax(z):
    """Numerically stable softmax."""
    raise NotImplementedError


def softmax_jacobian(z):
    """Jacobian of the softmax."""
    raise NotImplementedError


def attention_stats(d, n_keys, scaled, trials, rng):
    """(mean largest weight, median Jacobian Frobenius norm) of random attention."""
    raise NotImplementedError
