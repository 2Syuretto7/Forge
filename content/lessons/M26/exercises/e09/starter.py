import numpy as np


def _ordered(x):
    raise NotImplementedError


def ulps_between(a, b):
    """Number of float64 steps from a to b."""
    raise NotImplementedError


def close(a, b, rel=1e-9, abs_tol=0.0):
    """Relative-or-absolute closeness test."""
    raise NotImplementedError


def relative_error(approx, exact):
    """|approx - exact| / |exact|."""
    raise NotImplementedError
