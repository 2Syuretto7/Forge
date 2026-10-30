import math


def _clean(units):
    raise NotImplementedError


def _combine(a, b, sign):
    raise NotImplementedError


class Quantity:
    """A number with units, such as Quantity(3.0, {"m": 1, "s": -1})."""

    def __init__(self, value, units=None):
        """Store value and units (a dict from unit name to power), without zero powers."""
        raise NotImplementedError

    def __mul__(self, other):
        """Quantity times Quantity (powers add) or times a plain number."""
        raise NotImplementedError

    def __rmul__(self, other):
        """A plain number times a Quantity."""
        raise NotImplementedError

    def __truediv__(self, other):
        """Quantity divided by Quantity (powers subtract) or by a plain number."""
        raise NotImplementedError

    def __add__(self, other):
        """Add quantities with equal units; ValueError otherwise."""
        raise NotImplementedError

    def __sub__(self, other):
        """Subtract quantities with equal units; ValueError otherwise."""
        raise NotImplementedError

    def __eq__(self, other):
        """Equal units and values within relative tolerance 1e-12."""
        raise NotImplementedError
