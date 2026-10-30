import numpy as np


def central_vec(f, x, h):
    """Elementwise central differences."""
    raise NotImplementedError


def max_rel_error(est, exact):
    """Largest relative error."""
    raise NotImplementedError


def compare_steps(n=1_000_000):
    """(max relative error with h = 1e-5, with the scaled step) for log."""
    raise NotImplementedError
