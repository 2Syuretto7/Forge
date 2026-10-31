import numpy as np


def _softmax(z):
    raise NotImplementedError


def estimates(z, r, n, rng, baseline_fn):
    """REINFORCE estimates with a baseline that may depend on the action."""
    raise NotImplementedError


def bias(z, r, baseline_fn, n, rng):
    """Largest deviation of the mean estimate from the exact gradient."""
    raise NotImplementedError
