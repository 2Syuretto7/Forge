import math


def _mul(a, b):
    return (a[0] * b[0] + a[1] * b[2], a[0] * b[1] + a[1] * b[3], a[2] * b[0] + a[3] * b[2], a[2] * b[1] + a[3] * b[3])


def fib_power(n):
    """F_n exactly by repeated squaring."""
    result, base = (1, 0, 0, 1), (1, 1, 1, 0)
    while n:
        if n & 1:
            result = _mul(result, base)
        base = _mul(base, base)
        n >>= 1
    return result[1]


def fib_binet(n):
    """Binet's formula in floating point."""
    s5 = math.sqrt(5)
    return round((((1 + s5) / 2) ** n - ((1 - s5) / 2) ** n) / s5)


def first_disagreement(limit=100):
    """First n where Binet's float formula is wrong."""
    for n in range(limit):
        if fib_power(n) != fib_binet(n):
            return n
    return None
