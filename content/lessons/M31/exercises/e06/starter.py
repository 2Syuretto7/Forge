import numpy as np


def _f(x):
    raise NotImplementedError


def fit_predict(x_train, y_train, deg, x_test):
    """Polynomial least-squares fit evaluated at x_test."""
    raise NotImplementedError


def decompose(deg, datasets, rng, x_test):
    """Bias squared, variance, noise and measured test error."""
    raise NotImplementedError
