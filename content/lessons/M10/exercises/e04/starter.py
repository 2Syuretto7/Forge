import numpy as np


def rotation(theta):
    """Counterclockwise rotation by theta."""
    raise NotImplementedError


def scaling(sx, sy):
    """Stretch the axes."""
    raise NotImplementedError


def shear(k):
    """(x, y) -> (x + k y, y)."""
    raise NotImplementedError


def reflection(phi):
    """Reflect across the line at angle phi."""
    raise NotImplementedError
