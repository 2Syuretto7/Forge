import math
import random


def p_shared(m, days=365):
    """Exact chance that two of m people share a birthday."""
    p = 1.0
    for i in range(m):
        p *= (days - i) / days
    return 1 - p


def p_shared_approx(m, days=365):
    """1 - exp(-m (m - 1) / (2 days))."""
    return 1 - math.exp(-m * (m - 1) / (2 * days))


def smallest_room(target, days=365):
    """Smallest m with p_shared(m) >= target."""
    m = 1
    while p_shared(m, days) < target:
        m += 1
    return m


def simulate_room(m, n, seed=0):
    """Fraction of n random rooms of m people with a shared birthday."""
    rng = random.Random(seed)
    hits = 0
    for _ in range(n):
        b = [rng.randrange(365) for _ in range(m)]
        hits += len(set(b)) < m
    return hits / n
