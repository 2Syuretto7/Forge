import math


class Interval:
    """A positive interval [lo, hi] for estimates with error bars."""

    def __init__(self, lo, hi):
        """Store lo and hi; ValueError unless 0 < lo <= hi."""
        if not 0 < lo <= hi:
            raise ValueError("need 0 < lo <= hi")
        self.lo = lo
        self.hi = hi

    def __mul__(self, other):
        """Product with another Interval or a positive number."""
        o = other if isinstance(other, Interval) else Interval(other, other)
        return Interval(self.lo * o.lo, self.hi * o.hi)

    def __truediv__(self, other):
        """Quotient by another Interval or a positive number."""
        o = other if isinstance(other, Interval) else Interval(other, other)
        return Interval(self.lo / o.hi, self.hi / o.lo)

    def mid(self):
        """The geometric midpoint sqrt(lo * hi)."""
        return math.sqrt(self.lo * self.hi)

    def factor(self):
        """sqrt(hi / lo): the interval is mid() times or divided by this."""
        return math.sqrt(self.hi / self.lo)

    def contains(self, x):
        """True when lo <= x <= hi."""
        return self.lo <= x <= self.hi
