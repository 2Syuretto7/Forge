import math
import numpy as np


def time_grid(T, steps, tmin=1e-3):
    """Geometric grid from T down to tmin."""
    raise NotImplementedError


def reverse_sample(score, n, T, steps, rng, tmin=1e-3):
    """Euler-Maruyama on the reverse-time SDE."""
    raise NotImplementedError


def w1(x, y):
    """One-dimensional Wasserstein distance between equal-sized samples."""
    raise NotImplementedError
