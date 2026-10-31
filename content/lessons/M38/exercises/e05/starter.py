import numpy as np


def _log_softmax(z):
    raise NotImplementedError


def train_dpo(ref_logp, N, beta, steps, lr=5.0):
    """Gradient descent on the DPO loss over softmax logits."""
    raise NotImplementedError


def prob_gap(z):
    """Largest minus second largest probability."""
    raise NotImplementedError


def loss_at(z, ref_logp, N, beta):
    """DPO loss."""
    raise NotImplementedError
