import numpy as np


def power_history(A, x0, k):
    """Unit vectors of power iteration, start included."""
    raise NotImplementedError


def settled(history, tol=1e-8):
    """Whether the last two vectors lie along the same line."""
    raise NotImplementedError


def shifted_top(A, shift, k, x0):
    """Eigenvalue of A found by power iteration on A + shift I."""
    raise NotImplementedError
