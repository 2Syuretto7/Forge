import math
import time


# provided
def single_loop(n):
    """Constant work n times."""
    s = 0
    for i in range(n):
        s += i
    return s


# provided
def double_loop(n):
    """Constant work n * n times."""
    s = 0
    for i in range(n):
        for j in range(n):
            s += j
    return s


def time_call(fn, n, min_time=0.02):
    """Seconds per call of fn(n), from batches that double until min_time."""
    raise NotImplementedError


def fit_slope(xs, ys):
    """Least-squares slope of (xs, ys)."""
    raise NotImplementedError


def measured_exponent(fn, ns):
    """Slope of log10(time) against log10(n)."""
    raise NotImplementedError
