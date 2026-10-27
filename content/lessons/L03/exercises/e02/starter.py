import numpy as np


def sweep(f, df, x, hs, method):
    """Absolute errors of the forward or central estimate for each step in hs."""
    raise NotImplementedError


def best_step(hs, errors):
    raise NotImplementedError


def predicted_best_step(fx, f2, eps, method):
    """Theoretical optimal step. f2 is f'' for "forward" and f''' for "central"."""
    raise NotImplementedError
