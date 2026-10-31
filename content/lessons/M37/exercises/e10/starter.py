import math
import numpy as np


def uniform_grid(T, steps, tmin=1e-3):
    """Equally spaced times from T down to tmin."""
    raise NotImplementedError


def geometric_grid(T, steps, tmin=1e-3):
    """Geometrically spaced times from T down to tmin."""
    raise NotImplementedError


def sample_on_grid(score, n, grid, rng):
    """Reverse-time Euler-Maruyama over a decreasing grid."""
    raise NotImplementedError


def quality(score, data, grids, n, rng):
    """W1 distance from the data for samples generated on each grid."""
    raise NotImplementedError
