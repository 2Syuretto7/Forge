import math

import numpy as np


def sqrt_error(n):
    """Largest error of the n-piece interpolant of sqrt on [0, 1]."""
    raise NotImplementedError


def predicted_sqrt_error(n):
    """sqrt(h) / 4 with h = 1/n."""
    raise NotImplementedError


def pieces_for_sqrt(tol):
    """Smallest n with predicted_sqrt_error(n) <= tol."""
    raise NotImplementedError
