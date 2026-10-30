import math


def e_compounding(n):
    """(1 + 1/n)**n."""
    raise NotImplementedError


def e_series(terms):
    """Sum of 1/k! for k = 0 .. terms - 1."""
    raise NotImplementedError


def terms_for_digits(d):
    """Smallest number of series terms within 10**-d of e."""
    raise NotImplementedError


def compounding_error(n):
    """e - (1 + 1/n)**n."""
    raise NotImplementedError
