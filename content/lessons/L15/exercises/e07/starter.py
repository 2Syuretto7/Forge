import numpy as np


def isoflop_minimum(N, L):
    """Runs at one compute budget: fit a parabola to loss against log N and return the model size
    at its vertex and the loss there."""
    raise NotImplementedError


def allocation_exponent(C, N_opt):
    """The exponent a in N_opt = k C^a, by a least-squares line in log-log coordinates."""
    raise NotImplementedError
