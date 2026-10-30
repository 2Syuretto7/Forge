import numpy as np


def relu_sum(x):
    """Sum of max(0, x_i)."""
    raise NotImplementedError


def relu_sum_grad(x):
    """Indicator of positive entries."""
    raise NotImplementedError


def check_at(x, h=1e-6):
    """Relative error of a central-difference check."""
    raise NotImplementedError


def safe_point(x, h=1e-6):
    """Move entries near 0 out to +-10h."""
    raise NotImplementedError
