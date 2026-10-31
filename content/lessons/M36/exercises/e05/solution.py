import numpy as np


def gumbel(shape, rng):
    """Standard Gumbel samples."""
    return -np.log(-np.log(rng.random(shape)))


def gumbel_max(z, n, rng):
    """Categorical samples by the Gumbel-max trick."""
    return np.argmax(np.asarray(z) + gumbel((n, len(z)), rng), axis=1)


def gumbel_softmax(z, tau, n, rng):
    """Relaxed one-hot samples."""
    y = (np.asarray(z) + gumbel((n, len(z)), rng)) / tau
    y = np.exp(y - y.max(axis=1, keepdims=True))
    return y / y.sum(axis=1, keepdims=True)


def mean_max_entry(Y):
    """Average largest entry per row."""
    return float(np.mean(np.max(Y, axis=1)))
