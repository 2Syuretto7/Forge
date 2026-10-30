import numpy as np


def hessian_from_grad(grad, x, h=1e-5):
    """Symmetrized central differences of the gradient."""
    raise NotImplementedError


def is_local_min(H, tol=1e-8):
    """All eigenvalues above tol."""
    raise NotImplementedError


def curvature_bound(H):
    """Largest eigenvalue."""
    raise NotImplementedError
