import math


def logsumexp(z):
    """ln sum e**z_j, shifted by the maximum."""
    raise NotImplementedError


def log_softmax(z):
    """z_i - LSE(z)."""
    raise NotImplementedError


def nll(z, target):
    """Minus the log-softmax of the target class."""
    raise NotImplementedError
