import numpy as np


def best_rank_r(M, r):
    """Truncated SVD of rank r."""
    raise NotImplementedError


def rank_r_error(M, r):
    """Relative Frobenius error of the best rank-r approximation."""
    raise NotImplementedError


def effective_rank(M, energy=0.9):
    """Smallest rank capturing the given fraction of the squared singular values."""
    raise NotImplementedError
