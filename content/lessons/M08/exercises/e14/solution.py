import math


def comb_float_factorials(n, k):
    """n choose k from float factorials (overflows for large n)."""
    return float(math.factorial(n)) / (float(math.factorial(k)) * float(math.factorial(n - k)))


def largest_float_factorial():
    """Largest n with float(n!) finite."""
    n = 1
    while True:
        try:
            float(math.factorial(n + 1))
        except OverflowError:
            return n
        n += 1


def comb_logs(n, k):
    """n choose k via log-gamma."""
    return math.exp(math.lgamma(n + 1) - math.lgamma(k + 1) - math.lgamma(n - k + 1))


def comb_exact(n, k):
    """Exact n choose k."""
    return math.comb(n, k)
