import math
import random
from fractions import Fraction


def p_two_aces():
    """C(4, 2) / C(52, 2)."""
    raise NotImplementedError


def p_two_aces_ordered():
    """(4 * 3) / (52 * 51)."""
    raise NotImplementedError


def p_two_aces_mixed():
    """The mistake: ordered favourable over unordered possible."""
    raise NotImplementedError


def mismatch_factor(k):
    """k!: how many orders each hand of k cards has."""
    raise NotImplementedError


def simulate(n, seed=0):
    """Fraction of n random 2-card draws that are two aces."""
    raise NotImplementedError
