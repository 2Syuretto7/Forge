import numpy as np


def law(N, D, E, A, B, alpha, beta):
    """The parametric loss L(N, D) = E + A N^-alpha + B D^-beta."""
    return E + A * N ** -alpha + B * D ** -beta


def fit_for_exponents(alpha, beta, N, D, L):
    """With the exponents fixed, L = E + A N^-alpha + B D^-beta is linear in (E, A, B). Solve for
    them by least squares on the relative errors (each run's equation divided by its L). Return
    (E, A, B, sum of squared relative errors)."""
    raise NotImplementedError


def fit_parametric(N, D, L):
    """Search alpha and beta over 0.05, 0.07, ..., 0.95, then over a grid ten times finer
    (step 0.002) within 0.02 of the best pair. Return a dict with E, A, B, alpha, beta."""
    raise NotImplementedError
