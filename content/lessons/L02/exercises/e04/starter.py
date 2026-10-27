import numpy as np


def loglik(p, k, n):
    """k*log(p) + (n-k)*log(1-p) as a float, with 0*log(0) treated as 0."""
    raise NotImplementedError


def dloglik(p, k, n):
    """Derivative of loglik with respect to p."""
    raise NotImplementedError


def mle(k, n):
    """Maximum likelihood estimate of p."""
    raise NotImplementedError


def standard_error(k, n):
    """sqrt(p_hat * (1 - p_hat) / n)."""
    raise NotImplementedError
