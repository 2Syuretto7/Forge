import numpy as np


def _softmax(z):
    raise NotImplementedError


def gradient_variance(z, r, n, rng, b=0.0):
    """Total variance of single-sample REINFORCE estimates."""
    raise NotImplementedError


def train(means, offset, steps, lr, use_baseline, rng):
    """REINFORCE on a deterministic bandit; probability of the best arm at the end."""
    raise NotImplementedError
