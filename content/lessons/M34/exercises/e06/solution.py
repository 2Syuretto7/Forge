import numpy as np


def relu_gain(n_in, v):
    """Factor by which a linear layer plus ReLU multiplies the second moment."""
    return 0.5 * n_in * v


def he_variance(n_in):
    """He initialization variance."""
    return 2.0 / n_in


def xavier_variance(n_in):
    """Xavier initialization variance for a layer without a ReLU."""
    return 1.0 / n_in


def layer_second_moments(x, W):
    """Second moments of the input, the pre-activation and the ReLU output."""
    y = x @ W
    return float(np.mean(x**2)), float(np.mean(y**2)), float(np.mean(np.maximum(y, 0) ** 2))
