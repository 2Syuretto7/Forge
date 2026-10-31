import numpy as np


def round_mantissa(x, bits):
    """Round float32 values to the given number of fraction bits, ties to even."""
    u = np.asarray(x, dtype=np.float32).view(np.uint32)
    k = 23 - bits
    if k == 0:
        return u.view(np.float32).copy()
    lowest = (u >> np.uint32(k)) & np.uint32(1)
    u = u + (np.uint32((1 << (k - 1)) - 1) + lowest)
    u = u & np.uint32((0xFFFFFFFF >> k) << k)
    return u.view(np.float32)


def max_relative_error(bits):
    """Unit roundoff with this many fraction bits."""
    return 2.0 ** -(bits + 1)


def accumulate(increment, steps, bits):
    """Running total rounded to the given precision after every addition."""
    s = np.zeros(1, dtype=np.float32)
    inc = np.float32(increment)
    for _ in range(steps):
        s = round_mantissa(s + inc, bits)
    return float(s[0])
