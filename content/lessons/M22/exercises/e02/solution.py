import math


def bernoulli_pmf(k, p):
    """P(X = k) for a Bernoulli(p) variable."""
    if k == 1:
        return float(p)
    if k == 0:
        return float(1 - p)
    return 0.0


def binomial_pmf(k, n, p):
    """P(X = k) for a Binomial(n, p) variable."""
    if k < 0 or k > n:
        return 0.0
    return math.comb(n, k) * p**k * (1 - p) ** (n - k)


def poisson_pmf(k, lam):
    """P(X = k) for a Poisson(lam) variable."""
    if k < 0:
        return 0.0
    return math.exp(k * math.log(lam) - lam - math.lgamma(k + 1))


def cdf_from_pmf(pmf, k):
    """P(X <= k) for a pmf on 0, 1, 2, ..."""
    return sum(pmf(j) for j in range(0, k + 1))
