import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def score(theta, a):
    """The gradient of log softmax(theta)[a] with respect to theta: onehot(a) - p."""
    raise NotImplementedError


def exact_policy_gradient(theta, rewards):
    """The gradient of the expected reward sum_a p_a r_a, computed as E_a[r_a * score(theta, a)] by
    enumerating every action."""
    raise NotImplementedError


def reinforce_estimate(theta, rewards, n, seed, baseline=0.0):
    """The average of (r_a - baseline) * score(theta, a) over n actions sampled from softmax(theta)
    with np.random.default_rng(seed).choice."""
    raise NotImplementedError
