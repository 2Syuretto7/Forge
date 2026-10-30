import math


def rounded_rotation(theta, decimals):
    """(cos theta, sin theta) rounded to decimals places."""
    raise NotImplementedError


def scale_factor(c, s):
    """sqrt(c^2 + s^2)."""
    raise NotImplementedError


def radius_after(c, s, steps):
    """Length of (1, 0) after steps applications of [[c, -s], [s, c]]."""
    raise NotImplementedError


def predicted_radius(c, s, steps):
    """scale_factor ** steps."""
    raise NotImplementedError
