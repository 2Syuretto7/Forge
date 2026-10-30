import math


def rotate(p, theta):
    """p turned by theta about the origin."""
    raise NotImplementedError


def rotate_about(p, center, theta):
    """p turned by theta about center."""
    raise NotImplementedError


def rotation_matrix(theta):
    """[[cos, -sin], [sin, cos]]."""
    raise NotImplementedError


def apply(M, p):
    """Matrix (list of rows) times point."""
    raise NotImplementedError
