import math


def point_on_circle(theta, r=1.0):
    """(r cos theta, r sin theta)."""
    return r * math.cos(theta), r * math.sin(theta)


def angle_of(x, y):
    """Angle of (x, y) in (-pi, pi]."""
    return math.atan2(y, x)


def distance(p, q):
    """Distance between points p and q."""
    return math.sqrt((q[0] - p[0]) ** 2 + (q[1] - p[1]) ** 2)
