import numpy as np


def softmax_rows(S):
    """Softmax of every row, stable for large entries; -inf entries get weight 0."""
    m = S.max(axis=-1, keepdims=True)
    E = np.exp(S - m)
    return E / E.sum(axis=-1, keepdims=True)


def softmax_backward(P, dP):
    """Given P = softmax_rows(S) and dL/dP, return dL/dS."""
    return P * (dP - (dP * P).sum(axis=-1, keepdims=True))


def causal_mask(n):
    """Boolean (n, n) array, True where query i may not see key j (j > i)."""
    raise NotImplementedError


def attention(Q, K, V, causal=True, scale=True):
    """Single-head attention for Q, K of shape (n, d) and V of shape (n, dv). Return (O, P)."""
    raise NotImplementedError
