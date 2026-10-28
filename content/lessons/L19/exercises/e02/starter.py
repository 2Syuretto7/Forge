import numpy as np


def ce_with_z_loss(logits, y, z_coef):
    """Mean softmax cross-entropy of logits (n, V) against integer labels y, plus
    z_coef * mean(logsumexp(logits)^2). Return (loss, gradient with respect to logits)."""
    raise NotImplementedError
