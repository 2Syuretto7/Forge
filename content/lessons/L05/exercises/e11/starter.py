import numpy as np


def train_norms(X, y, lr=1.0, steps=20000, l2=0.0, every=1000):
    raise NotImplementedError


def train_confidence(X, y, w):
    """Return (min, max) probability assigned to the correct training label."""
    raise NotImplementedError
