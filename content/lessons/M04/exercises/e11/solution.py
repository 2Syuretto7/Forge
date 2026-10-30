import numpy as np


def fit_slope(xs, ys):
    """Least-squares slope of the points (xs, ys)."""
    xbar, ybar = sum(xs) / len(xs), sum(ys) / len(ys)
    num = sum((x - xbar) * (y - ybar) for x, y in zip(xs, ys))
    den = sum((x - xbar) ** 2 for x in xs)
    return num / den


def error_exponent(f, a, b, ns):
    """p in error ~ C n^-p, from a log-log fit."""
    x = np.linspace(a, b, 2000)
    errs = []
    for n in ns:
        knots = np.linspace(a, b, n + 1)
        errs.append(np.max(np.abs(f(x) - np.interp(x, knots, f(knots)))))
    return -fit_slope(list(np.log10(np.array(ns, dtype=float))), list(np.log10(np.array(errs))))
