import math
import numpy as np


def power_law(x, A, alpha):
    """A x^(-alpha)."""
    return A * np.asarray(x, dtype=float) ** (-alpha)


def loglog_slope(x1, y1, x2, y2):
    """Slope between two points on log-log axes."""
    return (math.log(y2) - math.log(y1)) / (math.log(x2) - math.log(x1))


def scale_factor(alpha, c):
    """Factor by which a power law changes when x is multiplied by c."""
    return c ** (-alpha)


def is_scale_invariant(f, xs, c, tol=1e-9):
    """Whether f(c x) / f(x) is constant over xs."""
    r = np.array([f(c * x) / f(x) for x in xs])
    return bool(np.max(np.abs(r - r[0])) <= tol * abs(r[0]))
