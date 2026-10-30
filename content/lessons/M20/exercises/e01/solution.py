import numpy as np


def _simpson(g, a, b, n):
    x = np.linspace(a, b, n + 1)
    w = np.ones(n + 1)
    w[1:-1:2] = 4
    w[2:-1:2] = 2
    return (b - a) / n / 3 * np.sum(w * g(x))


def midpoint_2d(f, ax, bx, ay, by, n):
    """Midpoint rule on an n by n grid."""
    hx, hy = (bx - ax) / n, (by - ay) / n
    xm = ax + hx * (np.arange(n) + 0.5)
    ym = ay + hy * (np.arange(n) + 0.5)
    X, Y = np.meshgrid(xm, ym, indexing="ij")
    return float(np.sum(f(X, Y)) * hx * hy)


def iterated(f, ax, bx, ay, by, n=200):
    """Simpson in y inside Simpson in x."""
    inner = lambda xs: np.array([_simpson(lambda y: f(x, y), ay, by, n) for x in xs])  # noqa: E731
    return float(_simpson(inner, ax, bx, n))


def over_triangle(f, n=400):
    """Integral over 0 <= y <= x <= 1."""
    inner = lambda xs: np.array([_simpson(lambda y: f(x, y), 0.0, x, n) if x > 0 else 0.0 for x in xs])  # noqa: E731
    return float(_simpson(inner, 0.0, 1.0, n))
