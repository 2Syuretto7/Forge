import math


def harmonic(n):
    """H_n as a float."""
    return sum(1 / k for k in range(1, n + 1))


def grouping_bound(k):
    """1 + k/2, a lower bound for H at 2**k."""
    return 1 + k / 2


def terms_to_exceed(x):
    """Smallest n with H_n > x."""
    total, n = 0.0, 0
    while total <= x:
        n += 1
        total += 1 / n
    return n


def log_estimate(n):
    """ln n + Euler's constant."""
    return math.log(n) + 0.5772156649
