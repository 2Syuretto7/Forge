import numpy as np


def tp_mlp_forward(x, W1s, b1s, W2s, b2):
    """A two-layer ReLU MLP split over len(W1s) ranks: rank r holds the columns W1s[r] (with bias
    b1s[r]) of the first layer and the matching rows W2s[r] of the second. Each rank computes its
    hidden slice and a partial output; summing the partial outputs (an all-reduce) and adding b2
    gives y. Return (y, cache) with cache = list of (x, pre-activation, hidden slice)."""
    cache, y = [], 0
    for W1, b1, W2 in zip(W1s, b1s, W2s):
        z = x @ W1 + b1
        h = np.maximum(z, 0)
        y = y + h @ W2
        cache.append((x, z, h))
    return y + b2, cache


def tp_mlp_backward(dy, cache, W1s, W2s):
    """Gradients for the split MLP: per rank (dW1, db1, dW2), the shared db2, and dx (the sum of
    every rank's partial dx: a second all-reduce). Return (per_rank, db2, dx)."""
    per_rank, dx = [], 0
    for (x, z, h), W1, W2 in zip(cache, W1s, W2s):
        dW2 = h.T @ dy
        dz = (dy @ W2.T) * (z > 0)
        per_rank.append((x.T @ dz, dz.sum(axis=0), dW2))
        dx = dx + dz @ W1.T
    return per_rank, dy.sum(axis=0), dx
