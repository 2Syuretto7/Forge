import numpy as np


def softmax(z):
    """Stable softmax."""
    raise NotImplementedError


def log_softmax(z):
    """Stable log-softmax."""
    raise NotImplementedError


def score(a, z):
    """Gradient of log pi_a in the logits."""
    raise NotImplementedError


def exact_grad(z, r):
    """Gradient of the expected reward in the logits."""
    raise NotImplementedError


def reinforce(z, r, n, rng):
    """Average of n REINFORCE estimates."""
    raise NotImplementedError
