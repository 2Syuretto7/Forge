import numpy as np


def mse(c, values, probs):
    """E[(X - c)^2]."""
    raise NotImplementedError


def dmse_dc(c, values, probs):
    """Derivative of mse with respect to c."""
    raise NotImplementedError


def best_constant(values, probs):
    """The minimizer of mse: the mean."""
    raise NotImplementedError


def mae(c, values, probs):
    """E|X - c|."""
    raise NotImplementedError


def best_constant_abs(values, probs):
    """A median: the smallest sorted value with cumulative probability at least 1/2."""
    raise NotImplementedError
