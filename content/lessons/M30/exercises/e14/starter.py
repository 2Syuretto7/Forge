import numpy as np


def naive_gibbs(r, tau):
    """Gibbs distribution as written."""
    raise NotImplementedError


def stable_gibbs(r, tau):
    """Gibbs distribution with the maximum subtracted."""
    raise NotImplementedError


def limit_low(r):
    """Uniform over the maximizers."""
    raise NotImplementedError


def limit_high(r):
    """Uniform."""
    raise NotImplementedError
