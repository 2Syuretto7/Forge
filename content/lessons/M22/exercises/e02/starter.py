import math


def bernoulli_pmf(k, p):
    """P(X = k) for a Bernoulli(p) variable."""
    raise NotImplementedError


def binomial_pmf(k, n, p):
    """P(X = k) for a Binomial(n, p) variable."""
    raise NotImplementedError


def poisson_pmf(k, lam):
    """P(X = k) for a Poisson(lam) variable."""
    raise NotImplementedError


def cdf_from_pmf(pmf, k):
    """P(X <= k) for a pmf on 0, 1, 2, ..."""
    raise NotImplementedError
