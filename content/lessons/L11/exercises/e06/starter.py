import numpy as np


def law(N, D, E, A, B, alpha, beta):
    """The parametric loss L(N, D) = E + A N^-alpha + B D^-beta."""
    return E + A * N ** -alpha + B * D ** -beta


def optimal_allocation(C, E, A, B, alpha, beta):
    """The compute-optimal (N, D, loss) for a budget of C = 6 N D FLOPs."""
    raise NotImplementedError


def dloss_dlogN(N, C, E, A, B, alpha, beta):
    """The derivative of L(N, C / 6N) with respect to log N at a fixed budget C."""
    raise NotImplementedError
