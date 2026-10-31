import numpy as np


def _x_of(Q, c, A, lam):
    raise NotImplementedError


def primal_value(Q, c, x):
    """(1/2) x^T Q x + c^T x."""
    raise NotImplementedError


def dual_value(Q, c, A, b, lam):
    """The dual function at lam."""
    raise NotImplementedError


def dual_grad(Q, c, A, b, lam):
    """Gradient of the dual function: A x(lam) - b."""
    raise NotImplementedError


def dual_ascent(Q, c, A, b, step, iters):
    """Projected gradient ascent on the dual; returns (lam, x(lam))."""
    raise NotImplementedError
