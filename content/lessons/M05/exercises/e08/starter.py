import math


def doubling_ratio(cost, n):
    """cost(2n) / cost(n)."""
    raise NotImplementedError


def exponent_estimate(cost, n):
    """log2 of the doubling ratio."""
    raise NotImplementedError


def classify(cost, n=1024):
    """Growth class from the doubling ratio at n."""
    raise NotImplementedError
