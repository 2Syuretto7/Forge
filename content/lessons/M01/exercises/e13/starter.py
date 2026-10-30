import numpy as np


def wrap_int32(n):
    """The value a signed 32-bit integer holds after the exact result n."""
    raise NotImplementedError


def overflows_int32(a, b):
    """True when a + b is outside the int32 range."""
    raise NotImplementedError


def numpy_sum_int32(values):
    """NumPy's int32 sum of the values, as a Python int."""
    raise NotImplementedError
