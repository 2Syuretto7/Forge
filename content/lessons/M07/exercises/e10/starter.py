import numpy as np


def rotation(theta, dtype):
    """Matrix turning row vectors by theta under points @ R."""
    raise NotImplementedError


def turn_many(points, steps, dtype):
    """Turn the points by 2 pi / steps, steps times, in dtype."""
    raise NotImplementedError


def drift(points, steps, dtype):
    """Largest absolute difference after a full circle in steps steps."""
    raise NotImplementedError
