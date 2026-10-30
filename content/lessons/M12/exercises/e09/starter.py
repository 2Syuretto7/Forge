import numpy as np


def line_fit(x, y):
    """(w0, w1) from the 2 by 2 normal equations."""
    raise NotImplementedError


def centered_fit(x, y):
    """(w0, w1) from deviations from the means."""
    raise NotImplementedError


def residual_checks(x, y, w0, w1):
    """(sum r, sum x r)."""
    raise NotImplementedError
