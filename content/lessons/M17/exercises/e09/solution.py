import math

import numpy as np


def gauss_trapezoid(n, L=6.0):
    """Trapezoid rule for exp(-x^2) on [-L, L]."""
    x = np.linspace(-L, L, n + 1)
    y = np.exp(-x * x)
    return float((2 * L / n) * (y.sum() - (y[0] + y[-1]) / 2))


def polar_inner(n, R=6.0):
    """Simpson's rule for r exp(-r^2) on [0, R]."""
    r = np.linspace(0, R, n + 1)
    w = np.ones(n + 1)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    return float(R / n / 3 * np.sum(w * r * np.exp(-r * r)))


def squared_check(n):
    """(trapezoid squared, 2 pi times the polar integral)."""
    return gauss_trapezoid(n) ** 2, 2 * math.pi * polar_inner(n)
