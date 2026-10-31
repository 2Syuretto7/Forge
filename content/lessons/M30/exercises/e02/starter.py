import numpy as np


def kkt_residuals(grad_f, grads_g, g_vals, lam):
    """The four KKT residuals."""
    raise NotImplementedError


def is_kkt(res, tol=1e-8):
    """Whether every residual is within tol."""
    raise NotImplementedError
