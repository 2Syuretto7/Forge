import numpy as np


def random_predictions(k, n, rng):
    """Random +1/-1 predictions."""
    return rng.integers(0, 2, size=(k, n)) * 2 - 1


def accuracy(pred, labels):
    """Fraction of matching labels."""
    return float(np.mean(np.asarray(pred) == np.asarray(labels)))


def adaptive_vote(P, labels):
    """Majority vote of the classifiers that beat 1/2 on these labels."""
    keep = (P == labels).mean(axis=1) > 0.5
    return np.sign(P[keep].sum(axis=0) + 0.5).astype(int)
