import numpy as np


def simpson(f, a, b, n):
    """Composite Simpson's rule."""
    if n % 2:
        raise ValueError("n must be even")
    x = np.linspace(a, b, n + 1)
    w = np.ones(n + 1)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    return float((b - a) / n / 3 * np.sum(w * f(x)))


def simpson_error_ratio(f, a, b, exact, n):
    """error(n) / error(2n)."""
    return abs(simpson(f, a, b, n) - exact) / abs(simpson(f, a, b, 2 * n) - exact)
