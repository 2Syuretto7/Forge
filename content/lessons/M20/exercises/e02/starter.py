import numpy as np


def mc_integral(f, box, n, seed=0):
    """(estimate, standard error) of the integral of f over the box."""
    raise NotImplementedError


def disc_area(n, seed=0):
    """Area of the unit disc by Monte Carlo."""
    raise NotImplementedError
