import numpy as np


def softmax(z):
    e = np.exp(z - np.max(z, axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def train_bandit(means, steps, lr, seed, batch=16):
    """REINFORCE on a bandit whose arm a pays means[a] plus N(0, 1) noise. Each step samples `batch`
    arms from softmax(theta), uses the batch's mean reward as the baseline, and ascends the
    average of (r - baseline) * (onehot(a) - p). Return the final probabilities."""
    rng = np.random.default_rng(seed)
    theta = np.zeros(len(means))
    for _ in range(steps):
        p = softmax(theta)
        acts = rng.choice(len(means), size=batch, p=p)
        r = np.asarray(means)[acts] + rng.normal(size=batch)
        b = r.mean()
        g = np.zeros_like(theta)
        for a, ri in zip(acts, r):
            s = -p.copy()
            s[a] += 1
            g += (ri - b) * s
        theta += lr * g / batch
    return softmax(theta)
