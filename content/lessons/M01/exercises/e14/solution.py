import numpy as np


def sum_floats(amounts):
    """Add the amounts in order as 64-bit floats."""
    total = 0.0
    for a in amounts:
        total += a
    return total


def sum_float32(amounts):
    """Add the amounts in order in 32-bit floats; return the final total."""
    return float(np.cumsum(np.asarray(amounts, dtype=np.float32), dtype=np.float32)[-1])


def sum_cents(amounts):
    """Exact total in integer cents."""
    return sum(round(a * 100) for a in amounts)


def drift_cents(amounts):
    """How many cents the 32-bit running total is off by."""
    return abs(sum_float32(amounts) * 100 - sum_cents(amounts))
