import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def score(theta, a):
    """The gradient of log softmax(theta)[a] with respect to theta: onehot(a) - p."""
    g = -softmax(theta)
    g[a] += 1
    return g


def exact_policy_gradient(theta, rewards):
    """The gradient of the expected reward sum_a p_a r_a, computed as E_a[r_a * score(theta, a)] by
    enumerating every action."""
    p = softmax(theta)
    return sum(p[a] * rewards[a] * score(theta, a) for a in range(len(theta)))


def reinforce_estimate(theta, rewards, n, seed, baseline=0.0):
    """The average of (r_a - baseline) * score(theta, a) over n actions sampled from softmax(theta)
    with np.random.default_rng(seed).choice."""
    rng = np.random.default_rng(seed)
    p = softmax(theta)
    acts = rng.choice(len(theta), size=n, p=p)
    return sum((rewards[a] - baseline) * score(theta, a) for a in acts) / n
