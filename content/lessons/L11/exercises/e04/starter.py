import numpy as np


def huber(r, delta):
    """Elementwise Huber loss and its derivative: r^2 / 2 for |r| <= delta, linear beyond."""
    raise NotImplementedError


def hoffmann_objective(theta, N, D, L, delta=1e-3):
    """theta = (a, b, e, alpha, beta), with A = exp(a), B = exp(b), E = exp(e). The predicted log
    loss is LSE(a - alpha log N, b - beta log D, e); return the sum over runs of
    huber(predicted - log L, delta) and its gradient with respect to theta."""
    raise NotImplementedError
