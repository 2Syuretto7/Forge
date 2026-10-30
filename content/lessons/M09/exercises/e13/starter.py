import numpy as np


def rank_by_dot(q, X):
    """Row indices by raw dot product, best first."""
    raise NotImplementedError


def rank_by_cosine(q, X):
    """Row indices by cosine similarity, best first."""
    raise NotImplementedError


def length_bias(q, X):
    """corr(lengths, dot scores) - corr(lengths, cosine scores)."""
    raise NotImplementedError


def make_trap(q, scale):
    """Row 0 along q (length 1); row 1 at 60 degrees from q with length scale."""
    raise NotImplementedError
