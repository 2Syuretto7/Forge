import numpy as np


def conds(degree, n=200):
    """(cond(A), cond(A^T A)) for the monomial basis on [0, 1]."""
    x = np.linspace(0, 1, n)
    A = np.vander(x, degree + 1, increasing=True)
    return float(np.linalg.cond(A)), float(np.linalg.cond(A.T @ A))


def digits_kept(cond):
    """About 16 - log10(cond), within [0, 16]."""
    return float(np.clip(16 - np.log10(cond), 0, 16))


def better_basis(degree, n=200):
    """cond of the Chebyshev design matrix on [-1, 1]."""
    t = 2 * np.linspace(0, 1, n) - 1
    return float(np.linalg.cond(np.polynomial.chebyshev.chebvander(t, degree)))
