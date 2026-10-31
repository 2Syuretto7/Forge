import numpy as np


def smooth_strong(A):
    """(L, mu) of the quadratic with Hessian A."""
    raise NotImplementedError


def condition_number(A):
    """L / mu."""
    raise NotImplementedError


def logistic_smoothness(X):
    """Upper bound on the smoothness of the average logistic loss."""
    raise NotImplementedError


def level_set_axes(A, c=1.0):
    """Half-axes of the level set (1/2) x^T A x = c, longest first."""
    raise NotImplementedError
