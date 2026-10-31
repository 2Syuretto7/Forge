import numpy as np


def online_softmax(x, block=4):
    """Softmax of a vector in one pass over blocks of `block` entries, keeping a running maximum m
    and a running sum l of exp(x - m); the sum is rescaled whenever the maximum grows. The final
    pass only divides. Return (p, m, l)."""
    raise NotImplementedError


def merge(m1, l1, m2, l2):
    """Combine the (max, sum) summaries of two disjoint parts of a vector."""
    raise NotImplementedError
