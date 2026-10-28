import numpy as np


def tempered_xent(logits, y, T):
    """Mean cross-entropy of softmax(logits / T) against labels y, and its gradient w.r.t. logits."""
    raise NotImplementedError


def entropy_at(logits, T):
    """Entropy, in nats, of softmax(logits / T) for one vector."""
    raise NotImplementedError
