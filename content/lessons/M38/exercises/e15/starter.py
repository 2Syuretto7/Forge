import math


def online_grad(t, C=3.0):
    """Gradient of the t-th online loss."""
    raise NotImplementedError


def run(amsgrad, steps=30000, C=3.0):
    """Projected Adam or AMSGrad on the online problem."""
    raise NotImplementedError


def average_loss_slope(C=3.0):
    """Slope of the average loss."""
    raise NotImplementedError
