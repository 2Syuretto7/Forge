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
    raise NotImplementedError


def wilson(k, n, z=1.96):
    """Wilson score interval."""
    raise NotImplementedError


def credible(k, n):
    """Central 95 percent posterior interval under a uniform prior."""
    raise NotImplementedError


def exact_coverage(interval, p, n):
    """Probability that interval(k, n) contains p, over k ~ Binomial(n, p)."""
    raise NotImplementedError
