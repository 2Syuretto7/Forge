import math
import numpy as np


def time_grid(T, steps, tmin=1e-3):
    """Geometric grid from T down to tmin."""
    return np.geomspace(T, tmin, steps + 1)


def reverse_sample(score, n, T, steps, rng, tmin=1e-3):
    """Euler-Maruyama on the reverse-time SDE."""
    ts = time_grid(T, steps, tmin)
    x = rng.standard_normal(n)
    for i in range(steps):
        h = ts[i] - ts[i + 1]
        x = x + h * (x + 2 * score(x, ts[i])) + math.sqrt(2 * h) * rng.standard_normal(n)
    return x


def w1(x, y):
    """One-dimensional Wasserstein distance between equal-sized samples."""
    return float(np.mean(np.abs(np.sort(x) - np.sort(y))))
