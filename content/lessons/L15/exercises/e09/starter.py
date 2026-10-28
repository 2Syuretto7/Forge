import numpy as np


def law(N, D, E, A, B, alpha, beta):
    """The parametric loss L(N, D) = E + A N^-alpha + B D^-beta."""
    return E + A * N ** -alpha + B * D ** -beta


def tokens_needed(N, target, E, A, B, alpha, beta):
    """Training tokens a model of N parameters needs to reach the target loss; inf if it cannot."""
    raise NotImplementedError


def cheapest_model(target, inference_tokens, E, A, B, alpha, beta):
    """Among models that reach the target loss, minimize training plus inference FLOPs,
    6 N D + 2 N inference_tokens, over N on 4001 log-spaced sizes from 1e6 to 1e13.
    Return (N, D, total FLOPs)."""
    raise NotImplementedError
