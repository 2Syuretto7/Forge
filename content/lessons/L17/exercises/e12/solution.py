import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def entropy(p):
    p = np.asarray(p)
    return float(-np.sum(p[p > 0] * np.log(p[p > 0])))


def train_with_kl(means, beta, steps=2000, lr=0.5):
    """Exact policy-gradient ascent (no sampling) on E[r] - beta KL(pi || pi_ref) for a bandit with
    arm rewards `means`, starting from the uniform reference. Return the final policy."""
    k = len(means)
    ref = np.full(k, 1 / k)
    theta = np.zeros(k)
    r = np.asarray(means, dtype=float)
    for _ in range(steps):
        p = softmax(theta)
        f = r - beta * np.log(p / ref)
        theta += lr * p * (f - p @ f)
    return softmax(theta)
