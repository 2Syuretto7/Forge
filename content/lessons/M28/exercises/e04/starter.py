import numpy as np


def _softplus(z):
    raise NotImplementedError


def _sigmoid(z):
    raise NotImplementedError


def logistic_loss(w, X, y):
    """Average logistic loss."""
    raise NotImplementedError


def logistic_grad(w, X, y):
    """Gradient of the average logistic loss."""
    raise NotImplementedError


def tangent_gap(f, grad, x, y_point):
    """f(y) - f(x) - grad(x) . (y - x)."""
    raise NotImplementedError
