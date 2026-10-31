import numpy as np


def grid_mean(f, d, k):
    """Midpoint-rule average of f over k^d grid points in the unit cube."""
    raise NotImplementedError


def mc_mean(f, d, n, rng):
    """Monte Carlo average of f over n uniform points in the unit cube."""
    raise NotImplementedError
