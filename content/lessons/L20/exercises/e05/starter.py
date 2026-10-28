import numpy as np


def best_rank_r(M, r):
    """The rank-r matrix closest to M in Frobenius norm: the truncated SVD (Eckart-Young)."""
    raise NotImplementedError


def relative_error(M, r):
    """|M - best_rank_r(M, r)|_F / |M|_F, from the singular values alone."""
    raise NotImplementedError


def rank_for(M, tol):
    """The smallest rank whose relative error is at most tol."""
    raise NotImplementedError
