import math

import numpy as np


def power_iteration(S, iters, seed=0):
    """(Rayleigh quotient, unit vector with its largest entry positive)."""
    raise NotImplementedError


def gap_ratio(S):
    """|lambda_2| / |lambda_1|."""
    raise NotImplementedError


def iterations_needed(ratio, tol):
    """Smallest k with ratio**k <= tol."""
    raise NotImplementedError
