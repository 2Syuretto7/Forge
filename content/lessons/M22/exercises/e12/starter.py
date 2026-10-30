import numpy as np


def layer_second_moments(depth, width, scale, activation="linear", batch=500, seed=0):
    """Mean squared activation after each of depth random layers."""
    raise NotImplementedError


def preserving_scale(activation):
    """Scale that keeps the second moment constant."""
    raise NotImplementedError


def predicted_factor(scale, activation, depth):
    """Predicted growth of the second moment over depth layers."""
    raise NotImplementedError
