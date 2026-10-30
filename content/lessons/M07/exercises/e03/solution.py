import math


def rotate(p, theta):
    """p turned by theta about the origin."""
    x, y = p
    c, s = math.cos(theta), math.sin(theta)
    return x * c - y * s, x * s + y * c


def rotate_about(p, center, theta):
    """p turned by theta about center."""
    x, y = rotate((p[0] - center[0], p[1] - center[1]), theta)
    return x + center[0], y + center[1]


def rotation_matrix(theta):
    """[[cos, -sin], [sin, cos]]."""
    c, s = math.cos(theta), math.sin(theta)
    return [[c, -s], [s, c]]


def apply(M, p):
    """Matrix (list of rows) times point."""
    return M[0][0] * p[0] + M[0][1] * p[1], M[1][0] * p[0] + M[1][1] * p[1]
