import numpy as np


def _R(theta):
    raise NotImplementedError


def turn_direct(points, k, delta):
    """One rotation by k * delta."""
    raise NotImplementedError


def turn_repeated(points, k, delta):
    """k rotations by delta."""
    raise NotImplementedError


def gap(points, k, delta):
    """Largest difference between the direct and the repeated turn."""
    raise NotImplementedError


def gap_growth(points, ks, delta):
    """Gaps for each k."""
    raise NotImplementedError
