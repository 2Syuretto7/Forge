import math


def one_sided(f, a, h=1e-7):
    """(left slope, right slope)."""
    return (f(a) - f(a - h)) / h, (f(a + h) - f(a)) / h


def has_corner(f, a, h=1e-7, tol=1e-4):
    """Whether the one-sided slopes differ."""
    l, r = one_sided(f, a, h)
    return abs(r - l) > tol


def relu_grad(x):
    """Framework convention: 1 if x > 0 else 0."""
    return 1.0 if x > 0 else 0.0


def abs_subgradients(x):
    """Interval of subgradients of |x|."""
    if x == 0:
        return (-1.0, 1.0)
    s = math.copysign(1.0, x)
    return (s, s)
