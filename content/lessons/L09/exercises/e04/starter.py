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
    return np.triu(np.ones((n, n), dtype=bool), k=1)


def attention(Q, K, V, causal=True, scale=True):
    """Single-head attention for Q, K of shape (n, d) and V of shape (n, dv). Return (O, P)."""
    S = Q @ K.T
    if scale:
        S = S / np.sqrt(Q.shape[-1])
    if causal:
        S = np.where(causal_mask(Q.shape[0]), -np.inf, S)
    P = softmax_rows(S)
    return P @ V, P


def split_heads(X, h):
    """(n, d) -> (h, n, d // h): head i gets columns i * d/h to (i + 1) * d/h."""
    raise NotImplementedError


def merge_heads(Y):
    """(h, n, dh) -> (n, h * dh), the inverse of split_heads."""
    raise NotImplementedError


def mha_forward(X, Wq, Wk, Wv, Wo, h, causal=True):
    """Multi-head self-attention: project, split into h heads, attend per head, merge, project.
    Return (Y, cache)."""
    raise NotImplementedError
