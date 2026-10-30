import numpy as np


def axis_check(f, x0, t=1e-2):
    """Whether f rises along every coordinate direction."""
    raise NotImplementedError


def hessian_eigen(H):
    """(eigenvalues, eigenvectors)."""
    raise NotImplementedError


def escape_direction(H):
    """Eigenvector of the most negative eigenvalue, or None."""
    raise NotImplementedError
