import math
import numpy as np


def power_iteration(S, iters, seed=0):
    """S: symmetric (n, n). Return (lam: float, v: (n,) unit vector, largest entry positive)."""
    raise NotImplementedError


def gap_ratio(S):
    """Return |lambda_2| / |lambda_1| for the two eigenvalues largest in magnitude."""
    raise NotImplementedError


def iterations_needed(ratio, tol):
    """Smallest integer k with ratio**k <= tol (0 < ratio < 1, 0 < tol < 1)."""
    raise NotImplementedError
