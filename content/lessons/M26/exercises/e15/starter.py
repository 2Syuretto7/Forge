import numpy as np


def _eliminate(A, b, pivot):
    raise NotImplementedError


def _back(U, c):
    raise NotImplementedError


def solve_no_pivot(A, b):
    """Gaussian elimination without pivoting."""
    raise NotImplementedError


def solve_partial_pivot(A, b):
    """Gaussian elimination with partial pivoting."""
    raise NotImplementedError


def growth_factor(A, pivot):
    """Largest entry during elimination over the largest entry of A."""
    raise NotImplementedError
