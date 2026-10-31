import numpy as np


def chord_violation(f, a, b, ts):
    """Largest amount by which f rises above its chord between a and b."""
    raise NotImplementedError


def search_violation(f, dim, trials, rng, scale=3.0):
    """Largest chord violation over random pairs of points."""
    raise NotImplementedError


def second_difference_min(f, lo, hi, n=2001):
    """Smallest second difference of f on a grid."""
    raise NotImplementedError
