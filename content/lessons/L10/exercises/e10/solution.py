import numpy as np


def smoothed_xent(logits, y, eps):
    """Cross-entropy against the smoothed target (1 - eps) onehot(y) + eps / V, mean over the batch,
    and its gradient w.r.t. the logits."""
    n, V = logits.shape
    Z = logits - logits.max(axis=1, keepdims=True)
    logp = Z - np.log(np.exp(Z).sum(axis=1, keepdims=True))
    target = np.full((n, V), eps / V)
    target[np.arange(n), y] += 1.0 - eps
    return -float(np.sum(target * logp) / n), (np.exp(logp) - target) / n
