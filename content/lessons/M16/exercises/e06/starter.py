import numpy as np


def second_diff(f, x, h=1e-4):
    """Central second difference."""
    raise NotImplementedError


def convex_on_grid(f, a, b, n=200, h=1e-4):
    """Whether the second difference is nonnegative on a grid."""
    raise NotImplementedError


def chord_check(f, a, b, trials=500, seed=0):
    """Whether random chords lie above the graph."""
    raise NotImplementedError
