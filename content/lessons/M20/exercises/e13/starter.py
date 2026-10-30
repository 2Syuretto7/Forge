import math

import numpy as np


def _phi(x):
    raise NotImplementedError


def wrong_density(y):
    """Without the Jacobian factor."""
    raise NotImplementedError


def right_density(y):
    """With the factor 1/2."""
    raise NotImplementedError


def total(density, lo=-30, hi=30, n=60_000):
    """Midpoint-rule integral."""
    raise NotImplementedError


def linear_density(y, A):
    """Density of A x for a standard normal pair x."""
    raise NotImplementedError
