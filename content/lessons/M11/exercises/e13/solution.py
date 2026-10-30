import numpy as np


def solve_both(eps):
    """(naive solution, pivoted solution)."""
    m = 1 / eps
    x2 = (2 - m * 1) / (1 - m * 1)
    naive = np.array([(1 - x2) / eps, x2])
    m = eps
    y2 = (1 - m * 2) / (1 - m * 1)
    pivot = np.array([2 - y2, y2])
    return naive, pivot


def exact_x1(eps):
    """1 / (1 - eps)."""
    return 1 / (1 - eps)


def digits(eps):
    """Correct significant digits of x1 for each method, capped at 16."""
    t = exact_x1(eps)
    out = []
    for x in solve_both(eps):
        rel = abs(x[0] - t) / abs(t)
        out.append(16.0 if rel == 0 else min(16.0, -np.log10(rel)))
    return tuple(out)
