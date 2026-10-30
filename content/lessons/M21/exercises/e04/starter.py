import numpy as np


def marginal(P, axes):
    """Sum out the variables not in axes."""
    raise NotImplementedError


def independent(P, i, j, tol=1e-12):
    """Independence of variables i and j."""
    raise NotImplementedError


def cond_independent(P, tol=1e-12):
    """Independence of variables 0 and 1 given variable 2."""
    raise NotImplementedError


def two_tests(prev, sens, spec):
    """Joint table of (test 1, test 2, disease)."""
    raise NotImplementedError
