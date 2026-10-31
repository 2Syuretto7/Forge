import numpy as np


class SGD:
    """SGD with optional heavy-ball momentum and L2 weight decay on the weights (keys starting with "W")."""

    def __init__(self, lr, momentum=0.0, weight_decay=0.0):
        raise NotImplementedError

    def step(self, params, grads, lr=None):
        raise NotImplementedError


class Adam:
    """Adam on a dict of arrays. weight_decay applies to the weights only, either decoupled
    (AdamW) or as an L2 term added to the gradient."""

    def __init__(self, lr, b1=0.9, b2=0.999, eps=1e-8, weight_decay=0.0, decoupled=True, bias_correction=True):
        raise NotImplementedError

    def step(self, params, grads, lr=None):
        raise NotImplementedError
