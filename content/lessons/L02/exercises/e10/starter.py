import numpy as np


def softmax(z):
    """Stable softmax of a 1-D array."""
    raise NotImplementedError


def nll(z, counts):
    """-sum_j counts_j * log softmax(z)_j as a float."""
    raise NotImplementedError


def grad_nll(z, counts):
    """Gradient of nll with respect to z, shape (K,)."""
    raise NotImplementedError


def mle_probs(counts):
    """Closed-form MLE of the category probabilities."""
    raise NotImplementedError
