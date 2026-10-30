def gap(p, q):
    """The integer |p^2 - 2 q^2|."""
    return abs(p * p - 2 * q * q)


def best_fraction(q):
    """(p, q) with p/q closest to the square root of 2."""
    return round(q * 2 ** 0.5), q


def smallest_gap(max_q):
    """Smallest gap over q = 1..max_q at the best p."""
    return min(gap(*best_fraction(q)) for q in range(1, max_q + 1))


def closest_fractions(max_q):
    """Fractions p/q (q <= max_q) with gap exactly 1, in increasing q."""
    return [best_fraction(q) for q in range(1, max_q + 1) if gap(*best_fraction(q)) == 1]
