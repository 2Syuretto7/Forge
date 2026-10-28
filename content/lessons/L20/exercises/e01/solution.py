import numpy as np


def masked_ce(logits, targets, mask):
    """Mean softmax cross-entropy of logits (T, V) against integer targets, over the positions where
    mask is 1 only. Return (loss, gradient with respect to logits), the gradient zero wherever the
    mask is 0."""
    m = logits.max(axis=1, keepdims=True)
    logp = logits - m - np.log(np.exp(logits - m).sum(axis=1, keepdims=True))
    n = mask.sum()
    rows = np.arange(len(targets))
    loss = -(logp[rows, targets] * mask).sum() / n
    g = np.exp(logp)
    g[rows, targets] -= 1
    return loss, g * mask[:, None] / n
