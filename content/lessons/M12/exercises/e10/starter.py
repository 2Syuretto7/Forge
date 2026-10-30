import numpy as np


def exact_data(degree, n=10000):
    """x on [0, 1] and the sum of x^k for k up to degree."""
    raise NotImplementedError


def coef_errors(degree):
    """(max coefficient error, normal equations; same, QR)."""
    raise NotImplementedError


def sweep(max_degree=20):
    """(degree, normal error, QR error) for each degree."""
    raise NotImplementedError
