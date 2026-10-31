import math
import numpy as np


def fit_rate(errors, start, stop):
    """Per-step rate from a log-linear fit over range(start, stop)."""
    raise NotImplementedError


def iterations_for(rho, factor):
    """Steps to shrink the error by factor."""
    raise NotImplementedError


def half_life(rho):
    """Steps to halve the error."""
    raise NotImplementedError
