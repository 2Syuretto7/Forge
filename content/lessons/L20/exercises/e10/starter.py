import numpy as np


def soften(logits, T):
    """softmax(logits / T)."""
    raise NotImplementedError


def entropy(p):
    raise NotImplementedError


def topk_teacher(p, k):
    """Keep the teacher's k largest probabilities and renormalize them (storing the teacher's full
    distribution for every token of a corpus costs vocabulary-size numbers per token)."""
    raise NotImplementedError
