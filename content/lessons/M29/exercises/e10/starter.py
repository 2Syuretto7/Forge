import time
import numpy as np


# provided
def make_data(n=10**6, d=8, seed=0):
    rng = np.random.default_rng(seed)
    X = rng.standard_normal((n, d))
    w = np.linspace(-1, 1, d)
    y = (rng.random(n) < 1 / (1 + np.exp(-X @ w))).astype(float)
    return X, y


# provided
TRUE_W = np.linspace(-1, 1, 8)


def _sig(z):
    raise NotImplementedError


def minibatch_grad(w, Xb, yb):
    """Logistic gradient on a batch."""
    raise NotImplementedError


def full_loss(w, X, y, chunk=100000):
    """Average logistic loss, chunk by chunk."""
    raise NotImplementedError


def train(X, y, method, epochs=2, batch=1000, lr=0.1, seed=0):
    """(weights, seconds) after training with the given optimizer."""
    raise NotImplementedError
