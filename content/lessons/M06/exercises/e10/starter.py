import numpy as np


def log_softmax(logits):
    """logits - logsumexp(logits), with the max shift."""
    raise NotImplementedError


def cross_entropy(logits, target):
    """Minus the log-softmax of the target."""
    raise NotImplementedError


def uniform_loss(V):
    """ln V."""
    raise NotImplementedError


def random_init_loss(V, scale, seed=0):
    """Mean cross-entropy over 100 random targets with logits scale * N(0, 1)."""
    raise NotImplementedError
