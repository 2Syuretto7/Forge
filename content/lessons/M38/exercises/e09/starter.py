import numpy as np


def _train(X, Y, W0, r, steps, lr=0.1, seed=0):
    raise NotImplementedError


def rank_sweep(X, Y, W0, ranks, steps=1500):
    """Loss and trainable fraction for each LoRA rank."""
    raise NotImplementedError


def full_loss(X, Y):
    """Loss of full least-squares fine-tuning."""
    raise NotImplementedError


def smallest_rank_within(sweep, full, slack=0.05):
    """Smallest rank whose loss is within slack of full fine-tuning."""
    raise NotImplementedError
