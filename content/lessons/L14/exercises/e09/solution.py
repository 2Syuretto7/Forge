import numpy as np


def tempered_xent(logits, y, T):
    """Mean cross-entropy of softmax(logits / T) against labels y, and its gradient w.r.t. logits."""
    Z = logits / T
    Z = Z - Z.max(axis=1, keepdims=True)
    logp = Z - np.log(np.exp(Z).sum(axis=1, keepdims=True))
    n = len(y)
    G = np.exp(logp)
    G[np.arange(n), y] -= 1.0
    return -float(np.mean(logp[np.arange(n), y])), G / (n * T)


def entropy_at(logits, T):
    """Entropy, in nats, of softmax(logits / T) for one vector."""
    z = logits / T
    z = z - z.max()
    p = np.exp(z) / np.exp(z).sum()
    return float(-np.sum(p * np.log(np.maximum(p, 1e-300))))
