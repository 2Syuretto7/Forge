import numpy as np


def design(x, degree):
    """Columns 1, x, ..., x^degree."""
    raise NotImplementedError


def polyfit_ls(x, y, degree):
    """Least-squares coefficients, lowest power first."""
    raise NotImplementedError


def polyval(c, x):
    """Horner's rule."""
    raise NotImplementedError
