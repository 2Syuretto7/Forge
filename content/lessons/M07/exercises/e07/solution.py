import math


def to_polar(x, y):
    """(r, theta)."""
    return math.hypot(x, y), math.atan2(y, x)


def to_cartesian(r, theta):
    """(x, y)."""
    return r * math.cos(theta), r * math.sin(theta)


def regular_polygon(n, r=1.0):
    """Vertices of a regular n-gon inscribed in a circle of radius r."""
    return [to_cartesian(r, 2 * math.pi * k / n) for k in range(n)]


def perimeter(points):
    """Length of the closed path through the points."""
    n = len(points)
    return sum(math.dist(points[i], points[(i + 1) % n]) for i in range(n))


def pi_estimate(n):
    """Half the perimeter of the regular n-gon in the unit circle."""
    return perimeter(regular_polygon(n)) / 2
