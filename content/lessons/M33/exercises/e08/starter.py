import numpy as np


def rsvd(A, k, p=10, q=1, rng=None):
    """Randomized SVD: (U, s, Vt) of rank k."""
    raise NotImplementedError


def top_singular_value(A):
    """Largest singular value."""
    raise NotImplementedError


def grad_top_singular_value(A):
    """Gradient of the largest singular value: u1 v1^T."""
    raise NotImplementedError
