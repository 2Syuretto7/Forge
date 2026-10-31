import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def score(theta, a):
    g = -softmax(theta)
    g[a] += 1
    return g


def estimator_stats(theta, rewards, baseline):
    """The exact mean and the total variance (sum over coordinates) of the single-sample estimator
    (r_a - baseline) * score(theta, a), computed by enumerating the actions."""
    raise NotImplementedError
