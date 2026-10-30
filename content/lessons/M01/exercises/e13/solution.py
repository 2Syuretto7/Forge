import numpy as np


def wrap_int32(n):
    """The value a signed 32-bit integer holds after the exact result n."""
    return ((n + 2 ** 31) % 2 ** 32) - 2 ** 31


def overflows_int32(a, b):
    """True when a + b is outside the int32 range."""
    s = a + b
    return not (-2 ** 31 <= s <= 2 ** 31 - 1)


def numpy_sum_int32(values):
    """NumPy's int32 sum of the values, as a Python int."""
    return int(np.array(values, dtype=np.int32).sum(dtype=np.int32))
