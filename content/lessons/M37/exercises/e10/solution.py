import math
import numpy as np


def uniform_grid(T, steps, tmin=1e-3):
    """Equally spaced times from T down to tmin."""
    return np.linspace(T, tmin, steps + 1)


def geometric_grid(T, steps, tmin=1e-3):
    """Geometrically spaced times from T down to tmin."""
    return np.geomspace(T, tmin, steps + 1)


def sample_on_grid(score, n, grid, rng):
    """Reverse-time Euler-Maruyama over a decreasing grid."""
    x = rng.standard_normal(n)
    for i in range(len(grid) - 1):
        h = grid[i] - grid[i + 1]
        x = x + h * (x + 2 * score(x, grid[i])) + math.sqrt(2 * h) * rng.standard_normal(n)
    return x


def quality(score, data, grids, n, rng):
    """W1 distance from the data for samples generated on each grid."""
    return [float(np.mean(np.abs(np.sort(sample_on_grid(score, n, g, rng)) - np.sort(data)))) for g in grids]
