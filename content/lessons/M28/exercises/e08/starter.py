import numpy as np


def objective(A, b, x):
    """(1/2) x^T A x - b^T x."""
    raise NotImplementedError


def solve_equality_qp(A, b, C, d):
    """Minimizer and multipliers of the equality-constrained quadratic."""
    raise NotImplementedError


def projected_minimum_check(A, b, C, d, x, trials, rng):
    """Smallest objective increase over random feasible perturbations."""
    raise NotImplementedError
