import math


def angle_2d(x, y):
    """Angle between two plane vectors, from their directions, in [0, pi]."""
    raise NotImplementedError


def dot_by_angle(x, y):
    """|x| |y| cos(angle)."""
    raise NotImplementedError


def law_of_cosines_gap(x, y):
    """|x - y|^2 - (|x|^2 + |y|^2 - 2 x . y)."""
    raise NotImplementedError
