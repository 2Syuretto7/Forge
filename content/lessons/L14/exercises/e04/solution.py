import numpy as np


def local_loss_grad(w, X, y):
    """Mean squared error 0.5 * mean((X w - y)^2) on one rank's shard, and its gradient."""
    r = X @ w - y
    return 0.5 * np.mean(r ** 2), X.T @ r / len(y)


def dp_step(w, shards, lr):
    """One synchronous data-parallel SGD step: every rank computes the gradient on its shard
    (X, y), the gradients are combined as the full-batch gradient would be (weight each by its
    shard size), and every rank applies the same update. Return the new w."""
    total = sum(len(y) for _, y in shards)
    g = sum(local_loss_grad(w, X, y)[1] * len(y) for X, y in shards) / total
    return w - lr * g
