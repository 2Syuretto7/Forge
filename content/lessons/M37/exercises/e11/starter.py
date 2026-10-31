import math
import numpy as np


def kde_score(X, t, centres, h):
    """Score of the noised kernel density estimate."""
    raise NotImplementedError


def dsm_loss(score, x0, rng, T=5.0, n_t=8):
    """Sigma-weighted denoising score-matching loss averaged over times."""
    raise NotImplementedError


def choose_bandwidth(train, valid, hs, rng):
    """Bandwidth with the smallest held-out score-matching loss."""
    raise NotImplementedError
