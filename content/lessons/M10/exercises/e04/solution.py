import numpy as np


def rotation(theta):
    """Counterclockwise rotation by theta."""
    c, s = np.cos(theta), np.sin(theta)
    return np.array([[c, -s], [s, c]])


def scaling(sx, sy):
    """Stretch the axes."""
    return np.array([[sx, 0.0], [0.0, sy]])


def shear(k):
    """(x, y) -> (x + k y, y)."""
    return np.array([[1.0, k], [0.0, 1.0]])


def reflection(phi):
    """Reflect across the line at angle phi."""
    c, s = np.cos(2 * phi), np.sin(2 * phi)
    return np.array([[c, s], [s, -c]])
