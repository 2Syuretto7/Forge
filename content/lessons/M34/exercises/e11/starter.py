import numpy as np


def relative_contrast(d, n, rng, queries=20):
    """Average (max - min) / min distance from random queries to n uniform points."""
    raise NotImplementedError


def expected_sq_distance(d):
    """Mean squared distance between independent uniform points in the unit cube."""
    raise NotImplementedError


def distance_cv(d, n, rng):
    """Coefficient of variation of distances between independent uniform pairs."""
    raise NotImplementedError
