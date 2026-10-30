import math


class Interval:
    """A positive interval [lo, hi] for estimates with error bars."""

    def __init__(self, lo, hi):
        """Store lo and hi; ValueError unless 0 < lo <= hi."""
        raise NotImplementedError

    def __mul__(self, other):
        """Product with another Interval or a positive number."""
        raise NotImplementedError

    def __truediv__(self, other):
        """Quotient by another Interval or a positive number."""
        raise NotImplementedError

    def mid(self):
        """The geometric midpoint sqrt(lo * hi)."""
        raise NotImplementedError

    def factor(self):
        """sqrt(hi / lo): the interval is mid() times or divided by this."""
        raise NotImplementedError

    def contains(self, x):
        """True when lo <= x <= hi."""
        raise NotImplementedError
