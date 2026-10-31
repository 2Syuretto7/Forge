import numpy as np


def sample_preferences(r, n, rng):
    """Count matrix of n Bradley-Terry comparisons."""
    raise NotImplementedError


def _log_softmax(z):
    raise NotImplementedError


def train_dpo(ref_logp, N, beta, steps=3000, lr=5.0):
    """Gradient descent on the DPO loss over softmax logits."""
    raise NotImplementedError


def tv(p, q):
    """Total variation distance."""
    raise NotImplementedError
