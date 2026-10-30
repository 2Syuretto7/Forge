import numpy as np


def contour_segments(f, level, box, n):
    """Marching-squares segments of f = level."""
    raise NotImplementedError


def max_cosine(segments, grad):
    """Largest |cos| between a segment and the gradient at its midpoint."""
    raise NotImplementedError
