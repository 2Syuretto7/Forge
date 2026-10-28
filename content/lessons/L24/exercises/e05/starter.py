import numpy as np


def masked_cross_entropy(logits, targets, mask):
    """Mean cross-entropy over the positions where mask is 1 (the response), for logits (T, V),
    integer targets (T,) and mask (T,). Return (loss, dlogits)."""
    raise NotImplementedError
