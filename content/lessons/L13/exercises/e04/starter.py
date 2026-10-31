import numpy as np


def naive_sum(values, dtype):
    """Add the values one by one, keeping the running sum in dtype."""
    raise NotImplementedError


def kahan_sum(values, dtype):
    """Compensated summation in dtype: carry the rounding error of each addition into the next."""
    raise NotImplementedError


def wide_accumulator_sum(values, dtype):
    """Store the inputs in dtype but accumulate in float32, as tensor cores do."""
    raise NotImplementedError
