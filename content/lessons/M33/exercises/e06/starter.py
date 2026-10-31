import numpy as np


def pcg(A, b, minv, tol=1e-8, max_iter=5000):
    """Jacobi-preconditioned conjugate gradient: (x, iterations)."""
    raise NotImplementedError


def badly_scaled(n, rng, spread=1e4):
    """A well-conditioned matrix with badly scaled variables."""
    raise NotImplementedError


def jacobi_condition(A):
    """Condition number after symmetric diagonal scaling."""
    raise NotImplementedError
