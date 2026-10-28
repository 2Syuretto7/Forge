import numpy as np


def target_update(d, rank, seed=0, decay=0.7):
    """A d x d update whose singular values fall geometrically, sigma_i = decay^i, for i < rank."""
    raise NotImplementedError


def error_by_rank(M, ranks):
    """Relative Frobenius error of the best rank-r approximation for each r."""
    raise NotImplementedError
