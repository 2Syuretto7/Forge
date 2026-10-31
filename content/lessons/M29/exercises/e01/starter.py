import numpy as np


def _softplus(z):
    raise NotImplementedError


def _sigmoid(z):
    raise NotImplementedError


def loss(w, X, y):
    """Average logistic loss."""
    raise NotImplementedError


def grad(w, X, y):
    """Gradient of the average logistic loss."""
    raise NotImplementedError


def gd(X, y, w0, step, iters):
    """Iterates of gradient descent."""
    raise NotImplementedError


def descent_lemma_holds(X, y, w0, iters):
    """Whether every step of size 1/L decreases f by at least |grad|^2 / (2L)."""
    raise NotImplementedError
