import numpy as np


def naive_softmax(z):
    """exp(z) / sum exp(z), silently."""
    with np.errstate(all="ignore"):
        e = np.exp(z)
        return e / e.sum()


def stable_softmax(z):
    """Softmax after subtracting the maximum."""
    e = np.exp(z - z.max())
    return e / e.sum()


def fails(z):
    """True when the naive softmax produces nan or infinity."""
    return not bool(np.all(np.isfinite(naive_softmax(z))))


def smallest_failing_shift(z):
    """Smallest integer c in 0..1000 with naive_softmax(z + c) failing, or None."""
    for c in range(1001):
        if fails(z + c):
            return c
    return None
