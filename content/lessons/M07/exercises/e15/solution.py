import math


def renormalize(c, s):
    """(c, s) divided by sqrt(c^2 + s^2)."""
    r = math.hypot(c, s)
    return c / r, s / r


def turn_with_renormalization(c, s, steps):
    """(1, 0) after steps applications of the renormalized matrix."""
    c, s = renormalize(c, s)
    x, y = 1.0, 0.0
    for _ in range(steps):
        x, y = c * x - s * y, s * x + c * y
    return x, y


def angle_error(c, s, theta):
    """Angle of the renormalized matrix minus the intended angle, in absolute value."""
    c, s = renormalize(c, s)
    return abs(math.atan2(s, c) - theta)
