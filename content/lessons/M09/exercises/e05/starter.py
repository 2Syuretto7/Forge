import numpy as np


def project(b, a):
    """Projection of b onto the line through a."""
    raise NotImplementedError


def residual(b, a):
    """b minus its projection onto a."""
    raise NotImplementedError


def component(b, a):
    """Signed length of the projection: a . b / |a|."""
    raise NotImplementedError
