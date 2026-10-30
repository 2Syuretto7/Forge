import math


def to_polar(x, y):
    """(r, theta)."""
    raise NotImplementedError


def to_cartesian(r, theta):
    """(x, y)."""
    raise NotImplementedError


def regular_polygon(n, r=1.0):
    """Vertices of a regular n-gon inscribed in a circle of radius r."""
    raise NotImplementedError


def perimeter(points):
    """Length of the closed path through the points."""
    raise NotImplementedError


def pi_estimate(n):
    """Half the perimeter of the regular n-gon in the unit circle."""
    raise NotImplementedError
