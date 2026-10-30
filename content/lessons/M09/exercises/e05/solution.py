import numpy as np


def project(b, a):
    """Projection of b onto the line through a."""
    return (a @ b) / (a @ a) * a


def residual(b, a):
    """b minus its projection onto a."""
    return b - project(b, a)


def component(b, a):
    """Signed length of the projection: a . b / |a|."""
    return float(a @ b / np.linalg.norm(a))
