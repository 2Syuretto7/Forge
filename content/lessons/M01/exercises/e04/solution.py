import math


def order_of_magnitude(x):
    """Return the int e with 10**e <= |x| < 10**(e+1)."""
    e = math.floor(math.log10(abs(x)))
    if abs(x) >= 10.0 ** (e + 1):
        e += 1
    elif abs(x) < 10.0 ** e:
        e -= 1
    return e


def nearest_power(x):
    """Return k such that 10**k is nearest to x on a log scale."""
    return round(math.log10(x))


def within_factor(a, b, k):
    """True when positive a and b are within a factor k of each other."""
    return max(a / b, b / a) <= k


def ladder(values):
    """Return [(order_of_magnitude(v), v)] sorted by value."""
    return [(order_of_magnitude(v), v) for v in sorted(values)]
