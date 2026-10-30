import numpy as np


def box_muller(u1, u2):
    """Two independent standard normals from two uniforms."""
    raise NotImplementedError


def sample_normal(n, seed=0):
    """n standard normals."""
    raise NotImplementedError


def check_moments(z):
    """(mean, variance, fraction within one standard deviation)."""
    raise NotImplementedError
