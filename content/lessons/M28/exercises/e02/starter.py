import numpy as np


def hessian_fd(f, x, h=1e-4):
    """Central-difference Hessian of f at x."""
    raise NotImplementedError


def min_eigenvalue(H):
    """Smallest eigenvalue of a symmetric matrix."""
    raise NotImplementedError


def convex_on_samples(f, points, h=1e-4, tol=1e-6):
    """Whether the Hessian is positive semidefinite at every sample point."""
    raise NotImplementedError
