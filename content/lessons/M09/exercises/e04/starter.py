import numpy as np


def l1(x):
    """Sum of absolute values."""
    raise NotImplementedError


def l2(x):
    """Euclidean length."""
    raise NotImplementedError


def linf(x):
    """Largest absolute value."""
    raise NotImplementedError


def in_unit_ball(x, p):
    """Whether the p-norm of x is at most 1."""
    raise NotImplementedError


def clip_by_norm(x, max_norm):
    """x scaled down to L2 length max_norm if longer."""
    raise NotImplementedError
