import numpy as np


def probe_loss(w, b, A, y, l2=1e-3):
    """A linear probe on activations A (n, d) for binary labels y: mean logistic loss of
    sigmoid(A w + b) plus l2 / 2 |w|^2. Return (loss, dw, db)."""
    raise NotImplementedError


def train_probe(A, y, steps=500, lr=1.0, l2=1e-3):
    raise NotImplementedError


def probe_accuracy(w, b, A, y):
    raise NotImplementedError
