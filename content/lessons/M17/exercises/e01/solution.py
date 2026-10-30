import math

import numpy as np


def riemann(f, a, b, n, where):
    """Riemann sum with n strips."""
    h = (b - a) / n
    off = {"left": 0.0, "right": 1.0, "mid": 0.5}[where]
    return float(h * np.sum(f(a + h * (np.arange(n) + off))))


def trapezoid(f, a, b, n):
    """Trapezoid rule."""
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return float(h * (y.sum() - (y[0] + y[-1]) / 2))


def observed_order(rule, f, a, b, exact, n):
    """log2(error with n / error with 2n)."""
    return math.log2(abs(rule(f, a, b, n) - exact) / abs(rule(f, a, b, 2 * n) - exact))
