import math
import numpy as np


def nll(w, s, X, y):
    """Average negative log-likelihood of a linear model with Gaussian noise."""
    raise NotImplementedError


def grad_w(w, s, X, y):
    """Gradient of nll with respect to w."""
    raise NotImplementedError


def fit(X, y):
    """Maximum-likelihood (w, sigma^2)."""
    raise NotImplementedError
