import numpy as np


def sweep(f, df, x, hs, method):
    """Absolute errors for each step."""
    raise NotImplementedError


def best_step(hs, errors):
    """Step with the smallest error."""
    raise NotImplementedError


def predicted_best_step(fx, f2, eps, method):
    """Theoretical optimal step."""
    raise NotImplementedError
