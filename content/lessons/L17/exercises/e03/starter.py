import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def train_bandit(means, steps, lr, seed, batch=16):
    """REINFORCE on a bandit whose arm a pays means[a] plus N(0, 1) noise. Each step samples `batch`
    arms from softmax(theta), uses the batch's mean reward as the baseline, and ascends the
    average of (r - baseline) * (onehot(a) - p). Return the final probabilities."""
    raise NotImplementedError
