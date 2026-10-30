import math


def strips_needed(C, p, tol):
    """Strips for C h^p <= tol on a unit interval."""
    raise NotImplementedError


def trapezoid_constant(max_f2, length):
    """C in error = C / n^2 for the trapezoid rule."""
    raise NotImplementedError


def trapezoid_strips(max_f2, length, tol):
    """Strips for the trapezoid rule."""
    raise NotImplementedError


def simpson_strips(max_f4, length, tol):
    """Even number of strips for Simpson's rule."""
    raise NotImplementedError
