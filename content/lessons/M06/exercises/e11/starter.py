import numpy as np


def overflow_threshold(dtype):
    """ln of the largest finite value of dtype."""
    raise NotImplementedError


def first_overflow(dtype):
    """Smallest integer n >= 0 with exp(n) infinite in dtype."""
    raise NotImplementedError


def safe_range(dtype):
    """(lo, hi): integers whose exp is finite and nonzero in dtype."""
    raise NotImplementedError
