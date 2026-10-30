import math

import numpy as np


def gauss_trapezoid(n, L=6.0):
    """Trapezoid rule for exp(-x^2) on [-L, L]."""
    raise NotImplementedError


def polar_inner(n, R=6.0):
    """Simpson's rule for r exp(-r^2) on [0, R]."""
    raise NotImplementedError


def squared_check(n):
    """(trapezoid squared, 2 pi times the polar integral)."""
    raise NotImplementedError
