import random


def squaring_keeps_order(a, b):
    """For a < b: whether a^2 < b^2."""
    return a * a < b * b


def find_counterexample(trials=1000, seed=0):
    """First random pair a < b with a^2 >= b^2, or None."""
    rnd = random.Random(seed)
    for _ in range(trials):
        a, b = sorted((rnd.uniform(-10, 10), rnd.uniform(-10, 10)))
        if a < b and not squaring_keeps_order(a, b):
            return a, b
    return None


def safe_to_square(a, b):
    """True when both are non-negative, so a < b implies a^2 < b^2."""
    return a >= 0 and b >= 0
