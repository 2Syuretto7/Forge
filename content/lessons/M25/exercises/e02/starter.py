import numpy as np


def rate_mle(x):
    """Maximum-likelihood estimate of an exponential rate."""
    raise NotImplementedError


def rate_unbiased(x):
    """Unbiased estimate of an exponential rate."""
    raise NotImplementedError


def simulate_rate_bias(n, lam, trials, seed=0):
    """(average MLE - lam, average unbiased estimate - lam)."""
    raise NotImplementedError
