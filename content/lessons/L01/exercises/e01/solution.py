import numpy as np


def dot(x, y):
    """x, y: shape (d,) floats. Return a float."""
    return float(np.sum(np.asarray(x, dtype=float) * np.asarray(y, dtype=float)))


def norm(x):
    """x: shape (d,). Return the Euclidean length as a float."""
    return float(np.sqrt(dot(x, x)))


def cosine_similarity(x, y):
    """Return cos(angle) between x and y as a float."""
    return dot(x, y) / (norm(x) * norm(y))


def angle_degrees(x, y):
    """Return the angle between x and y in degrees, in [0, 180]."""
    c = np.clip(cosine_similarity(x, y), -1.0, 1.0)
    return float(np.degrees(np.arccos(c)))
