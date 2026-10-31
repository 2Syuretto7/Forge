import numpy as np


def per_example_grads(W, X, y):
    Z = X @ W
    Z = Z - Z.max(axis=1, keepdims=True)
    P = np.exp(Z)
    P /= P.sum(axis=1, keepdims=True)
    P[np.arange(len(y)), y] -= 1.0
    return X[:, :, None] * P[:, None, :]


def minibatch_grad_stats(W, X, y, B, draws=2000, seed=0):
    G = per_example_grads(W, X, y)
    full = G.mean(axis=0)
    idx = np.random.default_rng(seed).integers(0, len(y), size=(draws, B))
    est = G[idx].mean(axis=1)
    mean_err = float(np.linalg.norm(est.mean(axis=0) - full))
    var = float(np.mean(np.sum((est - full) ** 2, axis=(1, 2))))
    return mean_err, var
