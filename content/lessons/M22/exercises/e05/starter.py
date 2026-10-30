import numpy as np


def marginals(joint):
    """(P(X = x_i), P(Y = y_j))."""
    raise NotImplementedError


def covariance(joint, xs, ys):
    """Cov(X, Y)."""
    raise NotImplementedError


def correlation(joint, xs, ys):
    """Correlation coefficient of X and Y."""
    raise NotImplementedError


def var_of_sum(joint, xs, ys):
    """Var(X + Y) from the joint table."""
    raise NotImplementedError
