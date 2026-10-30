import numpy as np


def fit_exponential(x, y):
    """(a, b) for y ~ a * b**x, from a line through ln y against x."""
    slope, icept = np.polyfit(x, np.log(y), 1)
    return float(np.exp(icept)), float(np.exp(slope))


def fit_power(x, y):
    """(c, p) for y ~ c * x**p, from a line through ln y against ln x."""
    slope, icept = np.polyfit(np.log(x), np.log(y), 1)
    return float(np.exp(icept)), float(slope)
