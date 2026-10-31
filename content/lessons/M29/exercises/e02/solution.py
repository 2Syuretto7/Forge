import math
import numpy as np


def fit_rate(errors, start, stop):
    """Per-step rate from a log-linear fit over range(start, stop)."""
    k = np.arange(start, stop)
    return float(np.exp(np.polyfit(k, np.log(np.asarray(errors, dtype=float)[start:stop]), 1)[0]))


def iterations_for(rho, factor):
    """Steps to shrink the error by factor."""
    return math.ceil(math.log(factor) / -math.log(rho))


def half_life(rho):
    """Steps to halve the error."""
    return math.log(2) / -math.log(rho)
