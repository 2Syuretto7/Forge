import numpy as np


def directional(grad, x, u):
    """Slope of f in the direction of u."""
    raise NotImplementedError


def steepest(grad, x):
    """Unit direction of steepest ascent."""
    raise NotImplementedError


def numerical_directional(f, x, u, h=1e-6):
    """Central difference along u."""
    raise NotImplementedError
