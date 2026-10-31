import math
import numpy as np


def power_law(x, A, alpha):
    """A x^(-alpha)."""
    raise NotImplementedError


def loglog_slope(x1, y1, x2, y2):
    """Slope between two points on log-log axes."""
    raise NotImplementedError


def scale_factor(alpha, c):
    """Factor by which a power law changes when x is multiplied by c."""
    raise NotImplementedError


def is_scale_invariant(f, xs, c, tol=1e-9):
    """Whether f(c x) / f(x) is constant over xs."""
    raise NotImplementedError
