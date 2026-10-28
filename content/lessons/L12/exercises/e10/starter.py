import numpy as np


def fused_cross_entropy(logits, y, block=8):
    """Mean cross-entropy computed per row in one pass over vocabulary blocks with a running max and
    sum (no full softmax array), and its gradient (softmax - onehot) / B written once.
    Return (loss, dlogits)."""
    raise NotImplementedError
