import numpy as np


def ce_from_probs(z, y):
    """Cross-entropy through probabilities."""
    raise NotImplementedError


def ce_from_logits(z, y):
    """Cross-entropy straight from the logits."""
    raise NotImplementedError


def first_failure(dtype):
    """Smallest integer logit gap that makes ce_from_probs infinite."""
    raise NotImplementedError
