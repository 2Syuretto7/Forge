import numpy as np


def ce_with_z_loss(logits, y, z_coef):
    """Mean softmax cross-entropy of logits (n, V) against integer labels y, plus
    z_coef * mean(logsumexp(logits)^2). Return (loss, gradient with respect to logits)."""
    m = logits.max(axis=1, keepdims=True)
    lse = (m + np.log(np.exp(logits - m).sum(axis=1, keepdims=True)))[:, 0]
    p = np.exp(logits - lse[:, None])
    n = len(y)
    loss = np.mean(lse - logits[np.arange(n), y]) + z_coef * np.mean(lse ** 2)
    g = p.copy()
    g[np.arange(n), y] -= 1
    g += 2 * z_coef * lse[:, None] * p
    return loss, g / n
