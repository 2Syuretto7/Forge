import numpy as np


def rank_k_approx(A, k):
    """Return the best rank-k approximation of A (same shape as A)."""
    raise NotImplementedError


def eckart_young_error(s, k):
    """s: all singular values, descending. Return ||A - A_k||_F."""
    raise NotImplementedError


def compression_ratio(m, n, k):
    """Return (m * n) / (k * (m + n + 1))."""
    raise NotImplementedError


def smallest_k(A, rel_tol):
    """Smallest k >= 0 with ||A - A_k||_F / ||A||_F <= rel_tol."""
    raise NotImplementedError
