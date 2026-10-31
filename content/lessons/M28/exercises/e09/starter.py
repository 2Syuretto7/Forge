import numpy as np


def gibbs(beta, K):
    """p_k proportional to exp(-beta k) on 0..K."""
    raise NotImplementedError


def mean_of(p):
    """Mean of a distribution on 0..K."""
    raise NotImplementedError


def max_entropy(m, K):
    """Maximum-entropy distribution on 0..K with mean m."""
    raise NotImplementedError


def entropy(p):
    """Entropy in nats."""
    raise NotImplementedError
