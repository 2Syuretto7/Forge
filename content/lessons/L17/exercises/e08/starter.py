import numpy as np


def dpo_loss(lw, ll, lw_ref, ll_ref, beta):
    """Mean over pairs of -log sigmoid(beta ((lw - lw_ref) - (ll - ll_ref))), with lw, ll the
    policy's log probabilities of the preferred and rejected responses and lw_ref, ll_ref the
    reference's. Return (loss, gradient with respect to lw, gradient with respect to ll)."""
    raise NotImplementedError


def tabular_dpo(ref, prefs, beta, steps=3000, lr=0.5):
    """A policy over K responses, pi = softmax(theta) with theta initialized to log(ref). prefs is
    a list of (winner, loser, count). Gradient descent on the count-weighted DPO loss through the
    log-softmax. Return the final pi."""
    raise NotImplementedError
