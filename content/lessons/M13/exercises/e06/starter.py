import numpy as np


def classify_form(S, tol=1e-12):
    """Sign pattern of the eigenvalues."""
    raise NotImplementedError


def cholesky(S):
    """Lower triangular L with L L^T = S; ValueError if S is not positive definite."""
    raise NotImplementedError


def is_pd(S):
    """Whether a Cholesky factorization exists."""
    raise NotImplementedError
