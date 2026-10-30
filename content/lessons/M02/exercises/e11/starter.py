import numpy as np


def fraction_small_det(n, t, seed=0):
    """Fraction of n random 2x2 matrices (entries uniform in [-1, 1]) with |det| < t."""
    raise NotImplementedError


def amplification(A, b, eps=1e-6):
    """Largest movement of the solution per unit nudge of b, over four axis nudges."""
    raise NotImplementedError
