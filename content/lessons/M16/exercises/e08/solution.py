import math


def mean_value_point(f, df, a, b, tol=1e-12):
    """c in (a, b) with f'(c) equal to the average slope."""
    slope = (f(b) - f(a)) / (b - a)
    g = lambda c: df(c) - slope  # noqa: E731
    lo, hi = a, b
    glo = g(lo)
    while hi - lo > tol:
        m = (lo + hi) / 2
        if (g(m) < 0) == (glo < 0):
            lo, glo = m, g(m)
        else:
            hi = m
    return (lo + hi) / 2


def taylor_remainder_point(x):
    """xi with e^x - 1 - x = e^xi x^2 / 2."""
    return math.log(2 * (math.exp(x) - 1 - x) / (x * x))
