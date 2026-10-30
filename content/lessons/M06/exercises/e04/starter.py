import math


# provided
def exp(x):
    """e**x by argument reduction and squaring."""
    k = 0
    while abs(x) / 2 ** k > 1:
        k += 1
    total, term = 0.0, 1.0
    for j in range(30):
        if j > 0:
            term *= (x / 2 ** k) / j
        total += term
    for _ in range(k):
        total = total * total
    return total


def ln(y):
    """Natural log of y > 0 by bisection on exp."""
    raise NotImplementedError


def log_base(y, b):
    """log_b y."""
    raise NotImplementedError


def digits(n):
    """Number of decimal digits of a positive integer n."""
    raise NotImplementedError
