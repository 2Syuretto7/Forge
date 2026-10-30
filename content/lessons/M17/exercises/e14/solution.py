import math

import numpy as np


def simpson_error(n):
    """Simpson error for sin(200 x) on [0, 1]."""
    x = np.linspace(0, 1, n + 1)
    w = np.ones(n + 1)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    return abs(float(np.sum(w * np.sin(200 * x)) / n / 3) - (1 - math.cos(200)) / 200)


def points_per_period(n, freq=200, length=1.0):
    """Sample points in one period."""
    return 2 * math.pi / freq * n / length


def first_good_n(tol=1e-8):
    """Smallest power of two meeting tol."""
    n = 2
    while simpson_error(n) >= tol:
        n *= 2
    return n
