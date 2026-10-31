import math
import numpy as np


# provided
def log_two_peaks(x, sep):
    return float(np.logaddexp(-0.5 * (x + sep / 2) ** 2, -0.5 * (x - sep / 2) ** 2))


def rw_standard_normal(step, d, n, rng):
    """Random-walk Metropolis on N(0, I_d): (samples, acceptance)."""
    raise NotImplementedError


def ess(x):
    """Effective sample size with pairwise truncation."""
    raise NotImplementedError


def ess_for_step(step, d, n, rng):
    """(acceptance, effective sample size of the first coordinate)."""
    raise NotImplementedError


def best_step(steps, d, n, rng):
    """The step with the largest effective sample size."""
    raise NotImplementedError


def mode_fraction(sep, step, n, rng):
    """Fraction of time a chain started in the left peak spends right of 0."""
    raise NotImplementedError
