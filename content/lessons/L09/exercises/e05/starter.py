import numpy as np


def rosenbrock_fg(p, a=1.0, b=100.0):
    """f(x, y) = (a - x)^2 + b (y - x^2)^2 and its gradient."""
    raise NotImplementedError


class Adam:
    """Adam for a single array. step(x, g) returns the updated array."""

    def __init__(self, lr, b1=0.9, b2=0.999, eps=1e-8, bias_correction=True):
        raise NotImplementedError

    def step(self, x, g):
        raise NotImplementedError
