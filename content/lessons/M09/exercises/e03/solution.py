import math


def angle_2d(x, y):
    """Angle between two plane vectors, from their directions, in [0, pi]."""
    d = abs(math.atan2(x[1], x[0]) - math.atan2(y[1], y[0]))
    return 2 * math.pi - d if d > math.pi else d


def dot_by_angle(x, y):
    """|x| |y| cos(angle)."""
    return math.hypot(*x) * math.hypot(*y) * math.cos(angle_2d(x, y))


def law_of_cosines_gap(x, y):
    """|x - y|^2 - (|x|^2 + |y|^2 - 2 x . y)."""
    sq = lambda v: sum(a * a for a in v)
    dot = sum(a * b for a, b in zip(x, y))
    return sq([a - b for a, b in zip(x, y)]) - (sq(x) + sq(y) - 2 * dot)
