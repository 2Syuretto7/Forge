import numpy as np


def cosine_distance(x, y):
    """1 - cos(angle)."""
    raise NotImplementedError


def angular_distance(x, y):
    """The angle in radians."""
    raise NotImplementedError


def triangle_violation(D, x, y, z):
    """D(x, z) - D(x, y) - D(y, z)."""
    raise NotImplementedError


def find_violation(D, trials=1000, seed=0):
    """A random triple of plane unit vectors violating the triangle inequality, or None."""
    raise NotImplementedError
