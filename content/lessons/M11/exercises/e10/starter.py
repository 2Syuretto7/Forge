import time

import numpy as np


def lu_fast(A):
    """(perm, L, U) with A[perm] = L U, one outer-product update per pivot."""
    raise NotImplementedError


def solve_fast(A, b):
    """Solve A x = b with lu_fast."""
    raise NotImplementedError


def compare(n, seed=0):
    """Times and relative residuals of solve_fast and np.linalg.solve."""
    raise NotImplementedError
