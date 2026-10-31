import numpy as np


def run_adam(grad, x0, steps, lr, b1=0.9, b2=0.999, eps=1e-12):
    """Adam trajectory."""
    raise NotImplementedError


def run_sgd(grad, x0, steps, lr):
    """Gradient descent trajectory."""
    raise NotImplementedError


def quadratic_grad(scales):
    """Gradient of sum_i s_i x_i^2 / 2."""
    raise NotImplementedError
