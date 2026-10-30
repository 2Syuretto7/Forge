import math


def _clean(units):
    return {k: p for k, p in units.items() if p != 0}


def _combine(a, b, sign):
    out = dict(a)
    for k, p in b.items():
        out[k] = out.get(k, 0) + sign * p
    return _clean(out)


class Quantity:
    """A number with units, such as Quantity(3.0, {"m": 1, "s": -1})."""

    def __init__(self, value, units=None):
        """Store value and units (a dict from unit name to power), without zero powers."""
        self.value = value
        self.units = _clean(dict(units or {}))

    def __mul__(self, other):
        """Quantity times Quantity (powers add) or times a plain number."""
        if isinstance(other, Quantity):
            return Quantity(self.value * other.value, _combine(self.units, other.units, 1))
        return Quantity(self.value * other, self.units)

    def __rmul__(self, other):
        """A plain number times a Quantity."""
        return self * other

    def __truediv__(self, other):
        """Quantity divided by Quantity (powers subtract) or by a plain number."""
        if isinstance(other, Quantity):
            return Quantity(self.value / other.value, _combine(self.units, other.units, -1))
        return Quantity(self.value / other, self.units)

    def __add__(self, other):
        """Add quantities with equal units; ValueError otherwise."""
        if self.units != other.units:
            raise ValueError(f"cannot add {other.units} to {self.units}")
        return Quantity(self.value + other.value, self.units)

    def __sub__(self, other):
        """Subtract quantities with equal units; ValueError otherwise."""
        if self.units != other.units:
            raise ValueError(f"cannot subtract {other.units} from {self.units}")
        return Quantity(self.value - other.value, self.units)

    def __eq__(self, other):
        """Equal units and values within relative tolerance 1e-12."""
        return isinstance(other, Quantity) and self.units == other.units and math.isclose(self.value, other.value, rel_tol=1e-12)
