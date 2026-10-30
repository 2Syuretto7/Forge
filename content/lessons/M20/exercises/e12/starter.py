import math


def grid_points(d, tol, C=1.0):
    """Points of a midpoint grid reaching tol."""
    raise NotImplementedError


def mc_points(tol, sigma=1.0):
    """Monte Carlo samples reaching tol."""
    raise NotImplementedError


def crossover_dimension(tol, C=1.0, sigma=1.0):
    """Smallest d where the grid costs more than Monte Carlo."""
    raise NotImplementedError
