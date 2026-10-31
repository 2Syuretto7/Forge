import math
import numpy as np


def range_finder(A, k, p, rng):
    """Orthonormal basis for the range of A @ Omega."""
    raise NotImplementedError


def power_range_finder(A, k, p, q, rng):
    """Range finder with q power iterations."""
    raise NotImplementedError


def projection_error(A, Q):
    """Frobenius norm of A - Q Q^T A."""
    raise NotImplementedError


def tail_norm(s, k):
    """Frobenius norm of the best rank-k approximation's error."""
    raise NotImplementedError


def hmt_factor(k, p):
    """Halko-Martinsson-Tropp factor for the expected Frobenius error."""
    raise NotImplementedError
