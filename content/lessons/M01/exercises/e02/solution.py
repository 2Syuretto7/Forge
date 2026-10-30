import math


def to_scientific(x):
    """Return (m, e) with x == m * 10**e, 1 <= |m| < 10 and e an int; (0.0, 0) for zero."""
    if x == 0:
        return 0.0, 0
    e = math.floor(math.log10(abs(x)))
    m = x / 10.0 ** e
    if abs(m) >= 10:
        m, e = m / 10, e + 1
    elif abs(m) < 1:
        m, e = m * 10, e - 1
    return m, e


def from_scientific(m, e):
    """Return m * 10**e as a float."""
    return m * 10.0 ** e


def format_scientific(x, digits):
    """Return x as a string like '3.00 x 10^8' with the given significant figures."""
    m, e = to_scientific(x)
    m = round(m, digits - 1)
    if abs(m) >= 10:
        m, e = m / 10, e + 1
    return f"{m:.{digits - 1}f} x 10^{e}"
