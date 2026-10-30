import math


def strips_needed(C, p, tol):
    """Strips for C h^p <= tol on a unit interval."""
    return math.ceil((C / tol) ** (1 / p))


def trapezoid_constant(max_f2, length):
    """C in error = C / n^2 for the trapezoid rule."""
    return length ** 3 * max_f2 / 12


def trapezoid_strips(max_f2, length, tol):
    """Strips for the trapezoid rule."""
    return math.ceil(math.sqrt(trapezoid_constant(max_f2, length) / tol))


def simpson_strips(max_f4, length, tol):
    """Even number of strips for Simpson's rule."""
    n = math.ceil((length ** 5 * max_f4 / (180 * tol)) ** 0.25)
    return n + (n % 2)
