import numpy as np


def first_step(b1, b2, lr=1.0):
    """Length of the uncorrected first Adam step per coordinate."""
    raise NotImplementedError


def step_lengths(g, lr, iters, b1=0.9, b2=0.999, bias_correction=True):
    """Per-step moves under a constant gradient."""
    raise NotImplementedError
