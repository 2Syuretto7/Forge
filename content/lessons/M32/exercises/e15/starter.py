import math
import numpy as np


# provided
def log_two_peaks(x, sep):
    return float(np.logaddexp(-0.5 * (x + sep / 2) ** 2, -0.5 * (x - sep / 2) ** 2))


def r_hat(chains):
    """Potential scale reduction factor."""
    raise NotImplementedError


def run_chains(starts, sep, step, n, rng):
    """One random-walk Metropolis chain on the two-peaked target per start."""
    raise NotImplementedError


def ess(x):
    """Effective sample size with pairwise truncation."""
    raise NotImplementedError
