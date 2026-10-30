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
    if y <= 0:
        raise ValueError("ln needs a positive number")
    lo, hi = -750.0, 750.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if exp(mid) < y:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def log_base(y, b):
    """log_b y."""
    return ln(y) / ln(b)


def digits(n):
    """Number of decimal digits of a positive integer n."""
    d = math.floor(log_base(n, 10)) + 1
    if n >= 10 ** d:
        d += 1
    elif n < 10 ** (d - 1):
        d -= 1
    return d
