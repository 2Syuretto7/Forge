import math

import numpy as np


def riemann(f, a, b, n, where):
    """Riemann sum with n strips."""
    raise NotImplementedError


def trapezoid(f, a, b, n):
    """Trapezoid rule."""
    raise NotImplementedError


def observed_order(rule, f, a, b, exact, n):
    """log2(error with n / error with 2n)."""
    raise NotImplementedError
