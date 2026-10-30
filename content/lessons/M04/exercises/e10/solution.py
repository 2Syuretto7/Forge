import numpy as np


def interp_error(f, a, b, n, m=1000):
    """Largest error of the n-piece interpolant at m random points of [a, b]."""
    knots = np.linspace(a, b, n + 1)
    x = np.random.default_rng(0).uniform(a, b, m)
    return float(np.max(np.abs(f(x) - np.interp(x, knots, f(knots)))))


def error_table(f, a, b, ns):
    """interp_error for each n in ns."""
    return [interp_error(f, a, b, n) for n in ns]


def shrink_factors(errors):
    """errors[i] / errors[i + 1]."""
    return [errors[i] / errors[i + 1] for i in range(len(errors) - 1)]
