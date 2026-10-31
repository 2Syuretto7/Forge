import numpy as np


def _ordered(x):
    i = int(np.float64(x).view(np.int64))
    return i if i >= 0 else -(i & 0x7FFFFFFFFFFFFFFF)


def ulps_between(a, b):
    """Number of float64 steps from a to b."""
    return abs(_ordered(b) - _ordered(a))


def close(a, b, rel=1e-9, abs_tol=0.0):
    """Relative-or-absolute closeness test."""
    return abs(a - b) <= max(rel * max(abs(a), abs(b)), abs_tol)


def relative_error(approx, exact):
    """|approx - exact| / |exact|."""
    return abs(approx - exact) / abs(exact)
