import numpy as np


def rayleigh(S, x):
    """x^T S x / x^T x."""
    return float(x @ S @ x / (x @ x))


def eig_weights(S, x):
    """(eigenvalues, squared coordinates in the eigenbasis over |x|^2)."""
    lam, Q = np.linalg.eigh(S)
    c = Q.T @ x
    return lam, c * c / (x @ x)
