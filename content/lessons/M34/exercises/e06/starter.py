import numpy as np


def relu_gain(n_in, v):
    """Factor by which a linear layer plus ReLU multiplies the second moment."""
    raise NotImplementedError


def he_variance(n_in):
    """He initialization variance."""
    raise NotImplementedError


def xavier_variance(n_in):
    """Xavier initialization variance for a layer without a ReLU."""
    raise NotImplementedError


def layer_second_moments(x, W):
    """Second moments of the input, the pre-activation and the ReLU output."""
    raise NotImplementedError
