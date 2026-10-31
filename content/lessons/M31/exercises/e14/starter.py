import numpy as np


def random_predictions(k, n, rng):
    """Random +1/-1 predictions."""
    raise NotImplementedError


def accuracy(pred, labels):
    """Fraction of matching labels."""
    raise NotImplementedError


def adaptive_vote(P, labels):
    """Majority vote of the classifiers that beat 1/2 on these labels."""
    raise NotImplementedError
