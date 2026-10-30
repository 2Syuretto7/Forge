import numpy as np


def overflow_threshold(dtype):
    """ln of the largest finite value of dtype."""
    return float(np.log(np.float64(np.finfo(dtype).max)))


def first_overflow(dtype):
    """Smallest integer n >= 0 with exp(n) infinite in dtype."""
    n = 0
    with np.errstate(over="ignore"):
        while not np.isinf(np.exp(np.array(n, dtype=dtype))):
            n += 1
    return n


def safe_range(dtype):
    """(lo, hi): integers whose exp is finite and nonzero in dtype."""
    hi = first_overflow(dtype) - 1
    lo = 0
    with np.errstate(under="ignore"):
        while np.exp(np.array(lo - 1, dtype=dtype)) > 0:
            lo -= 1
    return lo, hi
