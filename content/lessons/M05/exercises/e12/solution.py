import math


def remainder(r, n):
    """1/(1 - r) minus the sum of the first n terms."""
    return r ** n / (1 - r)


def terms_needed(r, eps):
    """Smallest n with remainder(r, n) < eps."""
    n = max(0, math.floor(math.log(eps * (1 - r)) / math.log(r)) + 1)
    while remainder(r, n) >= eps:
        n += 1
    while n > 0 and remainder(r, n - 1) < eps:
        n -= 1
    return n


def work_ratio(r1, r2, eps):
    """terms_needed(r2) / terms_needed(r1)."""
    return terms_needed(r2, eps) / terms_needed(r1, eps)
