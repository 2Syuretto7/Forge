import numpy as np


def softplus(x):
    """log(1 + e^x), stably."""
    raise NotImplementedError


def sigmoid(x):
    """1 / (1 + e^-x), stably for both signs."""
    raise NotImplementedError


def log_sigmoid(x):
    """log(sigmoid(x)), stably."""
    raise NotImplementedError
