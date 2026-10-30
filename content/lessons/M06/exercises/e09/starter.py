import math


def log_ticks(lo, hi):
    """Powers of ten between lo and hi inclusive."""
    raise NotImplementedError


def fit_line(xs, ys):
    """(slope, intercept, r2) of the least-squares line."""
    raise NotImplementedError


def straightness(xs, ys, xlog, ylog):
    """R^2 of a line fit after optional log10 of x and of y."""
    raise NotImplementedError


def best_axes(xs, ys):
    """"linear", "semilog" or "loglog", whichever is straightest."""
    raise NotImplementedError
