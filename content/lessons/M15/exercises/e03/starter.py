import numpy as np


def numerical_gradient(f, x, h=1e-6):
    """Central differences in every entry of x."""
    raise NotImplementedError


def relative_error(a, b):
    """Scale-free distance between two arrays."""
    raise NotImplementedError


def check_gradient(f, grad_f, x, h=1e-6, tol=1e-5):
    """(ok, err)."""
    raise NotImplementedError
