import numpy as np


def interp_error(f, a, b, n, m=1000):
    """Largest error of the n-piece interpolant at m random points of [a, b]."""
    raise NotImplementedError


def error_table(f, a, b, ns):
    """interp_error for each n in ns."""
    raise NotImplementedError


def shrink_factors(errors):
    """errors[i] / errors[i + 1]."""
    raise NotImplementedError
