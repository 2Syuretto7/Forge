import numpy as np


def tp_mlp_forward(x, W1s, b1s, W2s, b2):
    """A two-layer ReLU MLP split over len(W1s) ranks: rank r holds the columns W1s[r] (with bias
    b1s[r]) of the first layer and the matching rows W2s[r] of the second. Each rank computes its
    hidden slice and a partial output; summing the partial outputs (an all-reduce) and adding b2
    gives y. Return (y, cache) with cache = list of (x, pre-activation, hidden slice)."""
    raise NotImplementedError


def tp_mlp_backward(dy, cache, W1s, W2s):
    """Gradients for the split MLP: per rank (dW1, db1, dW2), the shared db2, and dx (the sum of
    every rank's partial dx: a second all-reduce). Return (per_rank, db2, dx)."""
    raise NotImplementedError
