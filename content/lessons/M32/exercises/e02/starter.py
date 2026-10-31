import numpy as np


def stationary_eig(P):
    """Left eigenvector of P for eigenvalue 1, normalized."""
    raise NotImplementedError


def stationary_power(P, tol=1e-13, max_iter=100000):
    """Stationary distribution by repeated multiplication."""
    raise NotImplementedError


def stationary_sim(P, n, rng, x0=0):
    """Fraction of time a simulated path spends in each state."""
    raise NotImplementedError


def two_state(a, b):
    """Stationary distribution of the two-state chain."""
    raise NotImplementedError
