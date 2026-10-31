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
    hits, done = 0, 0
    while done < n:
        k = min(chunk, n - done)
        hits += int(np.sum(rng.standard_normal(k) > a))
        done += k
    return hits


def is_rare(a, theta, n, rng):
    """Importance-sampling estimate of P(Z > a) and its standard error."""
    x = theta + rng.standard_normal(n)
    v = (x > a) * np.exp(-theta * x + 0.5 * theta * theta)
    return float(v.mean()), float(v.std(ddof=1) / math.sqrt(n))
