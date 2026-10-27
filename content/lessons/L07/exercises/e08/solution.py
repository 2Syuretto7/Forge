import numpy as np


def hinge_network(knots, values):
    knots = np.asarray(knots, dtype=float)
    values = np.asarray(values, dtype=float)
    slopes = np.diff(values) / np.diff(knots)
    w = np.ones(len(slopes))
    b = -knots[:-1]
    a = np.concatenate([[slopes[0]], np.diff(slopes)])
    return w, b, a, float(values[0])


def evaluate(params, x):
    w, b, a, c = params
    x = np.asarray(x, dtype=float)
    return c + np.maximum(0, np.outer(x, w) + b) @ a


def max_error(f, n_pieces):
    knots = np.linspace(-1, 1, n_pieces + 1)
    p = hinge_network(knots, f(knots))
    grid = np.linspace(-1, 1, 2001)
    return float(np.max(np.abs(evaluate(p, grid) - f(grid))))
