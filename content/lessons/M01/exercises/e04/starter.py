import math


def order_of_magnitude(x):
    """Return the int e with 10**e <= |x| < 10**(e+1)."""
    raise NotImplementedError


def nearest_power(x):
    """Return k such that 10**k is nearest to x on a log scale."""
    raise NotImplementedError


def within_factor(a, b, k):
    """True when positive a and b are within a factor k of each other."""
    raise NotImplementedError


def ladder(values):
    """Return [(order_of_magnitude(v), v)] sorted by value."""
    raise NotImplementedError
