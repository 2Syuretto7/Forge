import numpy as np


def fit_pure(C, L):
    """L = k C^-g by a log-log line; return (k, g)."""
    raise NotImplementedError


def fit_floor(C, L, grid=400):
    """L = E + k C^-g: for each E on `grid` + 1 evenly spaced values from 0 to just below min(L),
    fit log(L - E) by a line; keep the E with the smallest squared error. Return (E, k, g)."""
    raise NotImplementedError


def extrapolation_errors(C, L, target_C, target_L):
    """Relative errors (prediction / truth - 1) at target_C of the pure and the floor fits."""
    raise NotImplementedError
