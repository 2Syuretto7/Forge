import math
import random


def simulate(trial, n, seed=0):
    """Fraction of n runs of trial(rng) that return True."""
    rng = random.Random(seed)
    return sum(1 for _ in range(n) if trial(rng)) / n


def standard_error(p, n):
    """sqrt(p (1 - p) / n)."""
    return math.sqrt(p * (1 - p) / n)


def z_score(estimate, p, n):
    """Gap in standard errors."""
    return (estimate - p) / standard_error(p, n)


def roll_two_sum_seven(rng):
    """Two dice sum to 7."""
    return rng.randint(1, 6) + rng.randint(1, 6) == 7
