import numpy as np


def shell_fraction(n, eps):
    """Fraction of volume within eps of the surface."""
    raise NotImplementedError


def sample_ball(n, m, seed=0):
    """Uniform points in the unit ball."""
    raise NotImplementedError


def mean_radius(n, m=100_000, seed=0):
    """Average distance from the centre."""
    raise NotImplementedError
