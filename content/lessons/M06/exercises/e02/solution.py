import math


def e_compounding(n):
    """(1 + 1/n)**n."""
    return (1 + 1 / n) ** n


def e_series(terms):
    """Sum of 1/k! for k = 0 .. terms - 1."""
    total, term = 0.0, 1.0
    for k in range(terms):
        if k > 0:
            term /= k
        total += term
    return total


def terms_for_digits(d):
    """Smallest number of series terms within 10**-d of e."""
    n = 1
    while abs(e_series(n) - math.e) >= 10.0 ** -d:
        n += 1
    return n


def compounding_error(n):
    """e - (1 + 1/n)**n."""
    return math.e - e_compounding(n)
