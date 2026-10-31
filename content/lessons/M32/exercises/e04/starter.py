import numpy as np


def tv(p, q):
    """Total variation distance."""
    raise NotImplementedError


def lazy_cycle(n):
    """Lazy random walk on a ring."""
    raise NotImplementedError


def spectral_gap(P):
    """1 minus the second largest eigenvalue modulus."""
    raise NotImplementedError


def mixing_time(P, eps=0.25):
    """Worst-start steps until total variation at most eps."""
    raise NotImplementedError
