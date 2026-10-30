import numpy as np


def conds(degree, n=200):
    """(cond(A), cond(A^T A)) for the monomial basis on [0, 1]."""
    raise NotImplementedError


def digits_kept(cond):
    """About 16 - log10(cond), within [0, 16]."""
    raise NotImplementedError


def better_basis(degree, n=200):
    """cond of the Chebyshev design matrix on [-1, 1]."""
    raise NotImplementedError
