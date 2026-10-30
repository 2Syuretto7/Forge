import numpy as np


def hilbert(n, dtype=np.float64):
    """Return the n x n Hilbert matrix with entries 1 / (i + j + 1)."""
    raise NotImplementedError


def gauss_solve(A, b):
    """Gaussian elimination with partial pivoting in A's dtype. Return x."""
    raise NotImplementedError


def hilbert_error(n, dtype):
    """Relative error of solving H x = H @ ones in the given dtype."""
    raise NotImplementedError
