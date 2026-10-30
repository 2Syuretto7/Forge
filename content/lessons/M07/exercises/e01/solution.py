import math


def to_radians(deg):
    """Degrees to radians."""
    return deg * math.pi / 180


def to_degrees(rad):
    """Radians to degrees."""
    return rad * 180 / math.pi


def normalize(theta):
    """The equivalent angle in (-pi, pi]."""
    t = theta - 2 * math.pi * math.ceil((theta - math.pi) / (2 * math.pi))
    if t <= -math.pi:
        t += 2 * math.pi
    return t


def same_direction(a, b):
    """Whether a and b differ by a whole number of turns."""
    return abs(normalize(a - b)) < 1e-9
