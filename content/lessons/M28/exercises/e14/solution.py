import numpy as np


def f(x):
    """Tilted double well."""
    return (x * x - 1) ** 2 + 0.3 * x


def fprime(x):
    """Its derivative."""
    return 4 * x * (x * x - 1) + 0.3


def descend(x0, step=0.01, iters=5000):
    """Gradient descent from x0."""
    x = float(x0)
    for _ in range(iters):
        x -= step * fprime(x)
    return x


def basin_fraction(starts):
    """Fraction of starts that reach the global minimum."""
    return float(np.mean([descend(s) < 0 for s in starts]))


def _root(lo, hi):
    for _ in range(100):
        mid = 0.5 * (lo + hi)
        if np.sign(fprime(mid)) == np.sign(fprime(lo)):
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def minima():
    """The two local minima, sorted."""
    return _root(-2.0, -0.5), _root(0.5, 2.0)
