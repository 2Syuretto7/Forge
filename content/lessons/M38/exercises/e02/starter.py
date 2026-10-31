import numpy as np


def bt_prob(r, i, j):
    """Bradley-Terry probability that i beats j."""
    raise NotImplementedError


def bt_loglik(r, pairs):
    """Log-likelihood of observed (winner, loser) pairs."""
    raise NotImplementedError


def grad_bt_loglik(r, pairs):
    """Gradient of the log-likelihood in the rewards."""
    raise NotImplementedError


def count_matrix(pairs, K):
    """N[i, j] = number of times i beat j."""
    raise NotImplementedError
