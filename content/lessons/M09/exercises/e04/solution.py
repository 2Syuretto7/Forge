import numpy as np


def l1(x):
    """Sum of absolute values."""
    return float(np.sum(np.abs(x)))


def l2(x):
    """Euclidean length."""
    return float(np.sqrt(np.sum(x * x)))


def linf(x):
    """Largest absolute value."""
    return float(np.max(np.abs(x)))


def in_unit_ball(x, p):
    """Whether the p-norm of x is at most 1."""
    return {1: l1, 2: l2, "inf": linf}[p](x) <= 1


def clip_by_norm(x, max_norm):
    """x scaled down to L2 length max_norm if longer."""
    n = l2(x)
    return x * (max_norm / n) if n > max_norm else x
