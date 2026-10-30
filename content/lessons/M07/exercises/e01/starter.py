import math


def to_radians(deg):
    """Degrees to radians."""
    raise NotImplementedError


def to_degrees(rad):
    """Radians to degrees."""
    raise NotImplementedError


def normalize(theta):
    """The equivalent angle in (-pi, pi]."""
    raise NotImplementedError


def same_direction(a, b):
    """Whether a and b differ by a whole number of turns."""
    raise NotImplementedError
