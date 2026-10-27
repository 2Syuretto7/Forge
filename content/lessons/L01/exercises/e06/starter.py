import numpy as np


def loss(x, A, b):
    """Return ||Ax - b||^2 as a float."""
    raise NotImplementedError


def grad(x, A, b):
    """Return the gradient of the loss with respect to x, shape (n,)."""
    raise NotImplementedError


def gd_solve(A, b, steps):
    """Gradient descent from x = 0 with step 1 / (2 * sigma_max^2). Return x (n,)."""
    raise NotImplementedError
