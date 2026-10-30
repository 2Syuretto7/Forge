import numpy as np


def _simpson(g, a, b, n):
    raise NotImplementedError


def midpoint_2d(f, ax, bx, ay, by, n):
    """Midpoint rule on an n by n grid."""
    raise NotImplementedError


def iterated(f, ax, bx, ay, by, n=200):
    """Simpson in y inside Simpson in x."""
    raise NotImplementedError


def over_triangle(f, n=400):
    """Integral over 0 <= y <= x <= 1."""
    raise NotImplementedError
