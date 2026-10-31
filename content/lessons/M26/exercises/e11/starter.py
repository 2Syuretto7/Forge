import numpy as np


def round_mantissa(x, bits):
    """Round float32 values to the given number of fraction bits, ties to even."""
    raise NotImplementedError


def max_relative_error(bits):
    """Unit roundoff with this many fraction bits."""
    raise NotImplementedError


def accumulate(increment, steps, bits):
    """Running total rounded to the given precision after every addition."""
    raise NotImplementedError
