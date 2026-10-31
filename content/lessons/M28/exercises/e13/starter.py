import numpy as np


def gd_path(A, x0, step, iters):
    """Iterates of gradient descent on (1/2) x^T A x."""
    raise NotImplementedError


def growth_factor(A, step):
    """Largest per-step multiplier of the error."""
    raise NotImplementedError


def largest_stable_step(A):
    """2 / lambda_max."""
    raise NotImplementedError
