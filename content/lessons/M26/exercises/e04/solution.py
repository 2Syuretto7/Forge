import math
import numpy as np


def one_minus_cos(x):
    """(naive, stable) values of 1 - cos(x)."""
    return float(1 - np.cos(x)), float(2 * np.sin(x / 2) ** 2)


def expm1_over_x(x):
    """(naive, stable) values of (e^x - 1)/x."""
    return float((np.exp(x) - 1) / x), float(np.expm1(x) / x)


def small_root(a, b, c):
    """(naive, stable) smaller-magnitude root of a x^2 + b x + c."""
    d = math.sqrt(b * b - 4 * a * c)
    sgn = 1.0 if b > 0 else -1.0
    naive = (-b + sgn * d) / (2 * a)
    q = -0.5 * (b + sgn * d)
    return naive, c / q
