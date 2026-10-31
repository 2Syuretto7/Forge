import math
import numpy as np


# provided
def beta_quantiles(a, b, qs, m=20001):
    t = (np.arange(m) + 0.5) / m
    lp = (a - 1) * np.log(t) + (b - 1) * np.log1p(-t)
    cdf = np.cumsum(np.exp(lp - lp.max()))
    cdf /= cdf[-1]
    return [float(t[np.searchsorted(cdf, q)]) for q in qs]


def wald(k, n, z=1.96):
    """Wald interval."""
    p = k / n
    h = z * math.sqrt(p * (1 - p) / n)
    return p - h, p + h


def wilson(k, n, z=1.96):
    """Wilson score interval."""
    p = k / n
    d = 1 + z * z / n
    c = (p + z * z / (2 * n)) / d
    h = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return c - h, c + h


def credible(k, n):
    """Central 95 percent posterior interval under a uniform prior."""
    lo, hi = beta_quantiles(k + 1, n - k + 1, [0.025, 0.975])
    return lo, hi


def exact_coverage(interval, p, n):
    """Probability that interval(k, n) contains p, over k ~ Binomial(n, p)."""
    total = 0.0
    for k in range(n + 1):
        lo, hi = interval(k, n)
        if lo <= p <= hi:
            total += math.comb(n, k) * p**k * (1 - p) ** (n - k)
    return total
