import numpy as np


def sum_floats(amounts):
    """Add the amounts in order as 64-bit floats."""
    raise NotImplementedError


def sum_float32(amounts):
    """Add the amounts in order in 32-bit floats; return the final total."""
    raise NotImplementedError


def sum_cents(amounts):
    """Exact total in integer cents."""
    raise NotImplementedError


def drift_cents(amounts):
    """How many cents the 32-bit running total is off by."""
    raise NotImplementedError
