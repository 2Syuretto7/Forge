import math


def rounded_rotation(theta, decimals):
    """(cos theta, sin theta) rounded to decimals places."""
    return round(math.cos(theta), decimals), round(math.sin(theta), decimals)


def scale_factor(c, s):
    """sqrt(c^2 + s^2)."""
    return math.sqrt(c * c + s * s)


def radius_after(c, s, steps):
    """Length of (1, 0) after steps applications of [[c, -s], [s, c]]."""
    x, y = 1.0, 0.0
    for _ in range(steps):
        x, y = c * x - s * y, s * x + c * y
    return math.hypot(x, y)


def predicted_radius(c, s, steps):
    """scale_factor ** steps."""
    return scale_factor(c, s) ** steps
