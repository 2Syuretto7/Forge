import math
from fractions import Fraction


def riffle(deck, rng):
    """One Gilbert-Shannon-Reeds riffle shuffle."""
    raise NotImplementedError


def rising_sequences(perm):
    """Number of rising sequences of a deck of cards 0..n-1."""
    raise NotImplementedError


def eulerian_counts(n):
    """Number of permutations of n with r rising sequences, for r = 1..n."""
    raise NotImplementedError


def tv_after(k, n=52):
    """Exact total variation distance from uniform after k riffles."""
    raise NotImplementedError
