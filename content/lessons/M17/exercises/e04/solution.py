import numpy as np


def cumulative(f, a, b, n):
    """(grid, running trapezoid integral)."""
    x = np.linspace(a, b, n + 1)
    y = f(x)
    h = (b - a) / n
    return x, np.concatenate([[0.0], np.cumsum(h * (y[:-1] + y[1:]) / 2)])


def derivative_of_cumulative(x, F):
    """Central differences of F at interior points."""
    return (F[2:] - F[:-2]) / (x[2:] - x[:-2])
