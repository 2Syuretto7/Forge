import numpy as np


def naive_sum(values, dtype):
    """Add the values one by one, keeping the running sum in dtype."""
    s = dtype(0)
    for v in values:
        s = dtype(s + dtype(v))
    return s


def kahan_sum(values, dtype):
    """Compensated summation in dtype: carry the rounding error of each addition into the next."""
    s = dtype(0)
    c = dtype(0)
    for v in values:
        y = dtype(dtype(v) - c)
        t = dtype(s + y)
        c = dtype(dtype(t - s) - y)
        s = t
    return s


def wide_accumulator_sum(values, dtype):
    """Store the inputs in dtype but accumulate in float32, as tensor cores do."""
    return np.float32(np.sum(np.asarray(values, dtype=dtype).astype(np.float32)))
