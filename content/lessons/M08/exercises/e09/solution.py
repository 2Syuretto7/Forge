import math

C = math.comb


def full_houses():
    """Number of full houses."""
    return 13 * C(4, 3) * 12 * C(4, 2)


def flushes():
    """Flushes that are not straight flushes."""
    return 4 * (C(13, 5) - 10)


def two_pairs():
    """Hands with exactly two pairs."""
    return C(13, 2) * C(4, 2) ** 2 * 44


def probability(count):
    """count / C(52, 5)."""
    return count / C(52, 5)
