import itertools
import math


def union_size(sets):
    """Size of the union by inclusion-exclusion."""
    total = 0
    for r in range(1, len(sets) + 1):
        for group in itertools.combinations(sets, r):
            total += (-1) ** (r + 1) * len(set.intersection(*map(set, group)))
    return total


def count_divisible(n, divisors):
    """How many of 1..n are divisible by at least one divisor."""
    total = 0
    for r in range(1, len(divisors) + 1):
        for group in itertools.combinations(divisors, r):
            total += (-1) ** (r + 1) * (n // math.lcm(*group))
    return total
