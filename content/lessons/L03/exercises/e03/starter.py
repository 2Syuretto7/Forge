import numpy as np


def numerical_gradient(f, x, h=1e-6):
    """Central-difference gradient of scalar f at array x (any shape)."""
    raise NotImplementedError


def relative_error(a, b):
    raise NotImplementedError


def check_gradient(f, grad_f, x, h=1e-6, tol=1e-5):
    """Return (ok, err)."""
    raise NotImplementedError
