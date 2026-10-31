import numpy as np


def gibbs(r, tau):
    """Softmax of r / tau."""
    raise NotImplementedError


def objective(p, r, tau):
    """Expected reward plus tau times entropy."""
    raise NotImplementedError


def value(r, tau):
    """tau log sum exp(r / tau)."""
    raise NotImplementedError
