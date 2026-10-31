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
    p = softmax(theta)
    vals = [(rewards[a] - baseline) * score(theta, a) for a in range(len(theta))]
    mean = sum(p[a] * vals[a] for a in range(len(theta)))
    var = sum(p[a] * np.sum((vals[a] - mean) ** 2) for a in range(len(theta)))
    return mean, float(var)
