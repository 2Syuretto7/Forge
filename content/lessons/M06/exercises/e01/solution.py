def power_int(a, n):
    """a**n for an integer n, by repeated multiplication."""
    if n < 0:
        return 1 / power_int(a, -n)
    result = 1
    for _ in range(n):
        result *= a
    return result


def nth_root(a, n):
    """Positive n-th root of a > 0, by bisection on x**n."""
    lo, hi = 0.0, max(1.0, a)
    for _ in range(100):
        mid = (lo + hi) / 2
        if power_int(mid, n) < a:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def power_rational(a, p, q):
    """a**(p/q) = (a**(1/q))**p."""
    return power_int(nth_root(a, q), p)
