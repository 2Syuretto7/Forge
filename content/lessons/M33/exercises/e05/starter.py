import math
import numpy as np


def cg_iterations(A, b, tol=1e-8):
    """Iterations of CG to reach relative residual tol."""
    raise NotImplementedError


def cg_bound(kappa, k):
    """Chebyshev bound on the A-norm error ratio after k steps."""
    raise NotImplementedError


def iterations_predicted(kappa, tol):
    """Smallest k with cg_bound(kappa, k) <= tol."""
    raise NotImplementedError


def spd_with_spectrum(eigenvalues, rng):
    """Random symmetric matrix with the given eigenvalues."""
    raise NotImplementedError
