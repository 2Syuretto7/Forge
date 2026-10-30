import math
import random
from fractions import Fraction


def p_two_aces():
    """C(4, 2) / C(52, 2)."""
    return Fraction(math.comb(4, 2), math.comb(52, 2))


def p_two_aces_ordered():
    """(4 * 3) / (52 * 51)."""
    return Fraction(4 * 3, 52 * 51)


def p_two_aces_mixed():
    """The mistake: ordered favourable over unordered possible."""
    return Fraction(4 * 3, math.comb(52, 2))


def mismatch_factor(k):
    """k!: how many orders each hand of k cards has."""
    return math.factorial(k)


def simulate(n, seed=0):
    """Fraction of n random 2-card draws that are two aces."""
    rng = random.Random(seed)
    deck = ["A"] * 4 + ["x"] * 48
    return sum(1 for _ in range(n) if rng.sample(deck, 2) == ["A", "A"]) / n
