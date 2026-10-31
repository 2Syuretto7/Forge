import numpy as np


def adam_step(x, g, state, lr=1e-3, b1=0.9, b2=0.999, eps=1e-8):
    """One Adam update with bias correction."""
    raise NotImplementedError


def first_step_size(g, lr):
    """Size of the first Adam update."""
    raise NotImplementedError
