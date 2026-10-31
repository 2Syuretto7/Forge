import math
import numpy as np


# provided
def upper_tail(x):
    return 0.5 * math.erfc(x / math.sqrt(2))


# provided
def best_shift(a):
    def d(theta):
        phi = math.exp(-0.5 * (a + theta) ** 2) / math.sqrt(2 * math.pi)
        return math.exp(theta * theta) * (2 * theta * upper_tail(a + theta) - phi)

    lo, hi = 0.0, 2.0 * a
    for _ in range(60):
        mid = 0.5 * (lo + hi)
        lo, hi = (mid, hi) if d(mid) < 0 else (lo, mid)
    return 0.5 * (lo + hi)


def naive_hits(a, n, rng, chunk=10**6):
    """Number of n standard normal draws above a."""
    raise NotImplementedError


def is_rare(a, theta, n, rng):
    """Importance-sampling estimate of P(Z > a) and its standard error."""
    raise NotImplementedError
