import numpy as np


def spiked_samples(n, p, ell, rng):
    """Samples with one planted direction of variance 1 + ell."""
    raise NotImplementedError


def top_eig_and_overlap(X):
    """Top eigenvalue of X^T X / n and its eigenvector's squared overlap with e_1."""
    raise NotImplementedError


def bbp_top(ell, gamma):
    """Predicted top eigenvalue."""
    raise NotImplementedError


def bbp_overlap(ell, gamma):
    """Predicted squared overlap of the top eigenvector with the planted direction."""
    raise NotImplementedError
