import numpy as np


def example_grads(X, y, w):
    """Per-example gradients of (1/2)(x^T w - y)^2."""
    r = X @ w - y
    return X * r[:, None]


def full_grad(X, y, w):
    """Average gradient."""
    return example_grads(X, y, w).mean(axis=0)


def loss(X, y, w):
    """Average loss."""
    r = X @ w - y
    return float(0.5 * np.mean(r * r))


def minibatch_variance(X, y, w, batch, draws, rng):
    """Total variance of minibatch gradients drawn with replacement."""
    G = example_grads(X, y, w)
    idx = rng.integers(0, len(y), size=(draws, batch))
    return float(np.sum(np.var(G[idx].mean(axis=1), axis=0)))
