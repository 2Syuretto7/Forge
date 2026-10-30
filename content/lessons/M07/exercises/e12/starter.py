import numpy as np


def rope_batch(X, positions, base=10000):
    """Rotary encoding of each row of X at its position."""
    raise NotImplementedError


def relative_check(d, pairs, seed=0):
    """Largest |score(m, n) - score(m + s, n + s)| over random pairs and shifts."""
    raise NotImplementedError
