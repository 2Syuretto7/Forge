import numpy as np


def scalar_condition(f, df, x):
    """Relative condition number of f at x."""
    raise NotImplementedError


def hilbert(n):
    """The n by n Hilbert matrix."""
    raise NotImplementedError


def matrix_condition(A):
    """2-norm condition number."""
    raise NotImplementedError


def solve_error(n):
    """(relative error of solving H x = H 1, condition number of H)."""
    raise NotImplementedError
