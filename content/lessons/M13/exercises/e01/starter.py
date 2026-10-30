import math

import numpy as np


def is_eigenpair(A, lam, v, tol=1e-9):
    """Whether A v = lam v (v nonzero) up to a relative tolerance."""
    raise NotImplementedError


def char_poly2(A):
    """(1, -trace, det)."""
    raise NotImplementedError


def eig2_real(A):
    """Real eigenvalues of a 2 by 2 matrix, larger first."""
    raise NotImplementedError
