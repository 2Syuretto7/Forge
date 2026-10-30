import math


def to_scientific(x):
    """Return (m, e) with x == m * 10**e, 1 <= |m| < 10 and e an int; (0.0, 0) for zero."""
    raise NotImplementedError


def from_scientific(m, e):
    """Return m * 10**e as a float."""
    raise NotImplementedError


def format_scientific(x, digits):
    """Return x as a string like '3.00 x 10^8' with the given significant figures."""
    raise NotImplementedError
