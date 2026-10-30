import math


def grid_points(d, tol, C=1.0):
    """Points of a midpoint grid reaching tol."""
    m = math.ceil(math.sqrt(C / tol))
    return m ** d


def mc_points(tol, sigma=1.0):
    """Monte Carlo samples reaching tol."""
    return math.ceil((sigma / tol) ** 2)


def crossover_dimension(tol, C=1.0, sigma=1.0):
    """Smallest d where the grid costs more than Monte Carlo."""
    d = 1
    while grid_points(d, tol, C) <= mc_points(tol, sigma):
        d += 1
    return d
