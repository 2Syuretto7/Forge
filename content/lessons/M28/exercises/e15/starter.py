import numpy as np


def compose(g, h):
    """x -> g(h(x))."""
    raise NotImplementedError


def second_difference_min(f, lo, hi, n=4001):
    """Smallest second difference of f on a grid."""
    raise NotImplementedError


def is_nondecreasing(g, lo, hi, n=4001):
    """Whether g never decreases on a grid of [lo, hi]."""
    raise NotImplementedError
