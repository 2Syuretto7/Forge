import math


def doubling_ratio(cost, n):
    """cost(2n) / cost(n)."""
    return cost(2 * n) / cost(n)


def exponent_estimate(cost, n):
    """log2 of the doubling ratio."""
    return math.log2(doubling_ratio(cost, n))


def classify(cost, n=1024):
    """Growth class from the doubling ratio at n."""
    r = doubling_ratio(cost, n)
    if r < 1.01:
        return "constant"
    if r < 1.2:
        return "logarithmic"
    if r < 2.05:
        return "linear"
    if r < 2.4:
        return "n log n"
    if r < 5:
        return "quadratic"
    if r < 10:
        return "cubic"
    return "exponential"
