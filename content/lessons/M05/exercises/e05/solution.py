import math


def last_outside(seq, L, eps, max_n):
    """Largest n <= max_n with |seq(n) - L| >= eps, or 0."""
    last = 0
    for n in range(1, max_n + 1):
        if abs(seq(n) - L) >= eps:
            last = n
    return last


def geometric_N(r, eps):
    """Smallest n >= 1 with r**n < eps, for 0 < r < 1."""
    n = max(1, math.floor(math.log(eps) / math.log(r)) + 1)
    while r ** n >= eps:
        n += 1
    while n > 1 and r ** (n - 1) < eps:
        n -= 1
    return n


def harmonic_N(eps):
    """Smallest n with 1/n < eps."""
    n = math.floor(1 / eps) + 1
    while n > 1 and 1 / (n - 1) < eps:
        n -= 1
    return n
