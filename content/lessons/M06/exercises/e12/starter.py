import numpy as np


def fit_exponential(x, y):
    """(a, b) for y ~ a * b**x, from a line through ln y against x."""
    raise NotImplementedError


def fit_power(x, y):
    """(c, p) for y ~ c * x**p, from a line through ln y against ln x."""
    raise NotImplementedError
