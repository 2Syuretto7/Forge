import math


def renormalize(c, s):
    """(c, s) divided by sqrt(c^2 + s^2)."""
    raise NotImplementedError


def turn_with_renormalization(c, s, steps):
    """(1, 0) after steps applications of the renormalized matrix."""
    raise NotImplementedError


def angle_error(c, s, theta):
    """Angle of the renormalized matrix minus the intended angle, in absolute value."""
    raise NotImplementedError
