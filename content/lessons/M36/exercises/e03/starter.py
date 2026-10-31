import numpy as np


def _softmax(z):
    raise NotImplementedError


def estimates(z, r, n, rng, b=0.0):
    """Single-sample REINFORCE estimates with a constant baseline."""
    raise NotImplementedError


def total_variance(G):
    """Sum of per-component sample variances."""
    raise NotImplementedError


def optimal_baseline(z, r):
    """Constant baseline minimizing the total variance."""
    raise NotImplementedError
