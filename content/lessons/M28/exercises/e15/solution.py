import numpy as np


def compose(g, h):
    """x -> g(h(x))."""
    return lambda x: g(h(x))


def second_difference_min(f, lo, hi, n=4001):
    """Smallest second difference of f on a grid."""
    x = np.linspace(lo, hi, n)
    y = f(x)
    return float(np.min(y[:-2] - 2 * y[1:-1] + y[2:]))


def is_nondecreasing(g, lo, hi, n=4001):
    """Whether g never decreases on a grid of [lo, hi]."""
    y = g(np.linspace(lo, hi, n))
    return bool(np.all(np.diff(y) >= -1e-12))
