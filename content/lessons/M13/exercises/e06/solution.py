import numpy as np


def classify_form(S, tol=1e-12):
    """Sign pattern of the eigenvalues."""
    w = np.linalg.eigvalsh(S)
    pos, neg = np.any(w > tol), np.any(w < -tol)
    zero = np.any(np.abs(w) <= tol)
    if pos and neg:
        return "indefinite"
    if pos:
        return "positive semidefinite" if zero else "positive definite"
    if neg:
        return "negative semidefinite" if zero else "negative definite"
    return "positive semidefinite"


def cholesky(S):
    """Lower triangular L with L L^T = S; ValueError if S is not positive definite."""
    n = S.shape[0]
    L = np.zeros((n, n))
    for j in range(n):
        d = S[j, j] - L[j, :j] @ L[j, :j]
        if d <= 0:
            raise ValueError("not positive definite")
        L[j, j] = np.sqrt(d)
        for i in range(j + 1, n):
            L[i, j] = (S[i, j] - L[i, :j] @ L[j, :j]) / L[j, j]
    return L


def is_pd(S):
    """Whether a Cholesky factorization exists."""
    try:
        cholesky(S)
        return True
    except ValueError:
        return False
