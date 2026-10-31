import numpy as np


def is_reversible(P, pi, tol=1e-12):
    """Detailed balance pi_i P_ij = pi_j P_ji for all pairs."""
    raise NotImplementedError


def metropolis_matrix(pi, Q):
    """Metropolis-Hastings transition matrix for target pi and proposal Q."""
    raise NotImplementedError


def cycle_chain(n, p):
    """Clockwise step with probability p, otherwise stay."""
    raise NotImplementedError
