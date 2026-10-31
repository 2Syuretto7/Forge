import numpy as np


def dual_objective(alpha, X, y):
    """SVM dual objective."""
    raise NotImplementedError


def dual_grad(alpha, X, y):
    """Gradient of the dual objective."""
    raise NotImplementedError


def coordinate_ascent(X, y, C, epochs, rng):
    """Dual coordinate ascent; returns (alpha, w)."""
    raise NotImplementedError
