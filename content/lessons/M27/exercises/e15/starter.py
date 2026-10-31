import numpy as np


def kl(p, q):
    """KL(p || q) in nats."""
    raise NotImplementedError


def fit(samples, K, alpha=0.0):
    """Add-alpha estimate of a categorical distribution."""
    raise NotImplementedError


def heldout_ce(q, test):
    """Average negative log-probability of the test samples."""
    raise NotImplementedError


def best_alpha(train, test, K, alphas):
    """The alpha with the lowest held-out cross-entropy."""
    raise NotImplementedError
