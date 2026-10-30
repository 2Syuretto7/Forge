import math


def first_guess(a):
    """Cheap estimate of sqrt(a) from the floating-point exponent."""
    raise NotImplementedError


def iterations_to_full_precision(a, x0, tol=4e-16):
    """Newton steps until the relative error of sqrt(a) is below tol."""
    raise NotImplementedError
