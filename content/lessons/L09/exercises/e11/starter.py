import numpy as np


def softmax_rows(S):
    """Softmax of every row, stable for large entries; -inf entries get weight 0."""
    m = S.max(axis=-1, keepdims=True)
    E = np.exp(S - m)
    return E / E.sum(axis=-1, keepdims=True)


def softmax_backward(P, dP):
    """Given P = softmax_rows(S) and dL/dP, return dL/dS."""
    return P * (dP - (dP * P).sum(axis=-1, keepdims=True))


def saturation(d, scaled, n=16, seed=0):
    """Random queries and keys with unit-variance entries, shape (n, d). Return the mean over rows of
    the largest attention weight, and the mean absolute entry of the softmax Jacobian applied to a
    random upstream gradient (how much gradient reaches the scores)."""
    raise NotImplementedError
