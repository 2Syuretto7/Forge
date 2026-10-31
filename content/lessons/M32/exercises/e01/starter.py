import numpy as np


def check_stochastic(P):
    """True for a square matrix with nonnegative entries and unit row sums."""
    raise NotImplementedError


def distribution_after(pi0, P, n):
    """pi0 P^n."""
    raise NotImplementedError


def simulate(P, x0, n, rng):
    """A path of n + 1 states of the chain P starting at x0."""
    raise NotImplementedError
