import numpy as np


def softmax_t(logits, T=1.0):
    raise NotImplementedError


def top_k_filter(logits, k):
    """Keep the k largest logits; set the rest to -inf."""
    raise NotImplementedError


def top_p_filter(logits, p):
    """Keep the smallest set of tokens, taken in order of probability, whose total probability is at
    least p; set the rest to -inf."""
    raise NotImplementedError


def sample(logits, rng, T=1.0, k=None, p=None):
    """Temperature first, then the filters, then draw one token."""
    raise NotImplementedError
