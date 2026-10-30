import math

import numpy as np


def _lift(v):
    raise NotImplementedError


class Dual:
    """Forward mode: a value and its derivative."""

    def __init__(self, val, eps=0.0):
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

    def __lt__(self, o):
        raise NotImplementedError

    def __gt__(self, o):
        raise NotImplementedError


def _var(v):
    raise NotImplementedError


class Var:
    """Reverse mode: a value, its parents and an adjoint."""

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

    def __lt__(self, o):
        raise NotImplementedError

    def __gt__(self, o):
        raise NotImplementedError


def _apply(x, f, df):
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


def cos(x):
    """Cosine."""
    raise NotImplementedError


def tanh(x):
    """Hyperbolic tangent."""
    raise NotImplementedError


def sqrt(x):
    """Square root."""
    raise NotImplementedError


# provided
def target(x):
    a, b, c = x[0], x[1], x[2]
    s = a * b + sin(c)
    t = exp(-s * s / 4)
    u = log(1 + a * a) / (1 + t)
    v = 0
    for k in range(1, 4):
        v = v + (u ** k) / k
    if a > 0:
        w = sqrt(a * a + b * b + 1)
    else:
        w = cos(b) + 2
    y = v * w + tanh(c - a)
    z = y / (1 + b * b) + 3 * t
    return z


def grad_forward(f, x):
    """One dual-number pass per coordinate."""
    raise NotImplementedError


def grad_reverse(f, x):
    """One forward evaluation and one backward sweep."""
    raise NotImplementedError


def fd_grad(f, x, h=1e-6):
    """Central differences on plain floats."""
    raise NotImplementedError


def check(f, x):
    """Worst relative error of the exact gradients against central differences."""
    raise NotImplementedError
