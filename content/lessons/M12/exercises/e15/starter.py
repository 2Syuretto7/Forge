import numpy as np


def leverages(A):
    """Diagonal of the projection matrix."""
    raise NotImplementedError


def line_design(x):
    """Columns 1 and x."""
    raise NotImplementedError


def _slope(x, y):
    raise NotImplementedError


def influence(x, y, i):
    """Slope without point i minus slope with it."""
    raise NotImplementedError
