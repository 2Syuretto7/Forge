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
    reps = 1
    while True:
        t0 = time.perf_counter()
        for _ in range(reps):
            fn(n)
        elapsed = time.perf_counter() - t0
        if elapsed >= min_time:
            return elapsed / reps
        reps *= 2


def fit_slope(xs, ys):
    """Least-squares slope of (xs, ys)."""
    xbar, ybar = sum(xs) / len(xs), sum(ys) / len(ys)
    return sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys)) / sum((x - xbar) ** 2 for x in xs)


def measured_exponent(fn, ns):
    """Slope of log10(time) against log10(n)."""
    return fit_slope([math.log10(n) for n in ns], [math.log10(time_call(fn, n)) for n in ns])
