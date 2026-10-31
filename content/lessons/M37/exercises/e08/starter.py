import numpy as np


def _grid(T, steps, tmin):
    raise NotImplementedError


def flow_backward(score, x, T, steps, tmin=1e-3):
    """Probability-flow ODE from T down to tmin."""
    raise NotImplementedError


def flow_forward(score, x, T, steps, tmin=1e-3):
    """Probability-flow ODE from tmin up to T, undoing flow_backward."""
    raise NotImplementedError


def w1(x, y):
    """One-dimensional Wasserstein distance between equal-sized samples."""
    raise NotImplementedError
