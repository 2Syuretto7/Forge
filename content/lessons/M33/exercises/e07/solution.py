import math
import numpy as np


def range_finder(A, k, p, rng):
    """Orthonormal basis for the range of A @ Omega."""
    return np.linalg.qr(A @ rng.standard_normal((A.shape[1], k + p)))[0]


def power_range_finder(A, k, p, q, rng):
    """Range finder with q power iterations."""
    Q = range_finder(A, k, p, rng)
    for _ in range(q):
        Q = np.linalg.qr(A.T @ Q)[0]
        Q = np.linalg.qr(A @ Q)[0]
    return Q


def projection_error(A, Q):
    """Frobenius norm of A - Q Q^T A."""
    return float(np.linalg.norm(A - Q @ (Q.T @ A)))


def tail_norm(s, k):
    """Frobenius norm of the best rank-k approximation's error."""
    return float(np.sqrt(np.sum(np.asarray(s)[k:] ** 2)))


def hmt_factor(k, p):
    """Halko-Martinsson-Tropp factor for the expected Frobenius error."""
    return math.sqrt(1 + k / (p - 1))
