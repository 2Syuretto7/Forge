import numpy as np


def naive_softmax(z):
    """exp(z) / sum exp(z), silently."""
    raise NotImplementedError


def stable_softmax(z):
    """Softmax after subtracting the maximum."""
    raise NotImplementedError


def fails(z):
    """True when the naive softmax produces nan or infinity."""
    raise NotImplementedError


def smallest_failing_shift(z):
    """Smallest integer c in 0..1000 with naive_softmax(z + c) failing, or None."""
    raise NotImplementedError
