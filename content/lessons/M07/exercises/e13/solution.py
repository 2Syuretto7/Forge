import math


def sin_degrees(deg):
    """Sine of an angle given in degrees."""
    return math.sin(math.radians(deg))


def units_used(inputs, outputs):
    """"degrees", "radians" or "unknown"."""
    if all(abs(o - sin_degrees(i)) < 1e-9 for i, o in zip(inputs, outputs)):
        return "degrees"
    if all(abs(o - math.sin(i)) < 1e-9 for i, o in zip(inputs, outputs)):
        return "radians"
    return "unknown"


def suspicious(deg_inputs, outputs):
    """True when some output is far from the sine of its degree input."""
    return any(abs(o - sin_degrees(i)) > 0.01 for i, o in zip(deg_inputs, outputs))
