def gap(p, q):
    """The integer |p^2 - 2 q^2|."""
    raise NotImplementedError


def best_fraction(q):
    """(p, q) with p/q closest to the square root of 2."""
    raise NotImplementedError


def smallest_gap(max_q):
    """Smallest gap over q = 1..max_q at the best p."""
    raise NotImplementedError


def closest_fractions(max_q):
    """Fractions p/q (q <= max_q) with gap exactly 1, in increasing q."""
    raise NotImplementedError
