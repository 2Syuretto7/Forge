import numpy as np


def masked_ce(logits, targets, mask):
    """Mean softmax cross-entropy of logits (T, V) against integer targets, over the positions where
    mask is 1 only. Return (loss, gradient with respect to logits), the gradient zero wherever the
    mask is 0."""
    raise NotImplementedError
