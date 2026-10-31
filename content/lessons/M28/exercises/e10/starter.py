import numpy as np


def log_partition(theta):
    """log sum exp(theta)."""
    raise NotImplementedError


def grad_log_partition(theta):
    """Gradient of the log-partition: the softmax."""
    raise NotImplementedError


def nll(theta, counts):
    """Negative log-likelihood of category counts."""
    raise NotImplementedError


def fit(counts, steps=500, lr=1.0):
    """Gradient descent on the average negative log-likelihood."""
    raise NotImplementedError
