import numpy as np


def masked_cross_entropy(logits, targets, mask):
    """Mean cross-entropy over the positions where mask is 1 (the response), for logits (T, V),
    integer targets (T,) and mask (T,). Return (loss, dlogits)."""
    z = logits - logits.max(axis=1, keepdims=True)
    p = np.exp(z)
    p /= p.sum(axis=1, keepdims=True)
    n = mask.sum()
    rows = np.arange(len(targets))
    loss = -(np.log(p[rows, targets]) * mask).sum() / n
    g = p.copy()
    g[rows, targets] -= 1
    return float(loss), g * mask[:, None] / n
