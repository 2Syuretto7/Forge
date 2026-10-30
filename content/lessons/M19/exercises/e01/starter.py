import math


class Var:
    """A value with the recipe that produced it."""

    def __init__(self, value, parents=()):
        raise NotImplementedError

    def __add__(self, o):
        raise NotImplementedError

    __radd__ = __add__

    def __sub__(self, o):
        raise NotImplementedError

    def __rsub__(self, o):
        raise NotImplementedError

    def __mul__(self, o):
        raise NotImplementedError

    __rmul__ = __mul__

    def __truediv__(self, o):
        raise NotImplementedError

    def __rtruediv__(self, o):
        raise NotImplementedError

    def __neg__(self):
        raise NotImplementedError

    def __pow__(self, p):
        raise NotImplementedError


def exp(x):
    """e^x."""
    raise NotImplementedError


def log(x):
    """Natural logarithm."""
    raise NotImplementedError


def sin(x):
    """Sine."""
    raise NotImplementedError


def tanh(x):
    """Hyperbolic tangent."""
    raise NotImplementedError


def backward(out):
    """Fill .grad of every node with d out / d node."""
    raise NotImplementedError
