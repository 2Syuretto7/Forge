import numpy as np


def softmax(z):
    e = np.exp(z - z.max(axis=-1, keepdims=True))
    return e / e.sum(axis=-1, keepdims=True)


def full_attention(Q, K, V):
    """Causal single-head attention over a whole sequence (T, d)."""
    T, d = Q.shape
    s = Q @ K.T / np.sqrt(d)
    s = np.where(np.triu(np.ones((T, T), dtype=bool), 1), -np.inf, s)
    return softmax(s) @ V


def cached_attention(q, k, v, cache):
    """Attention for one new position: append k and v (shape (d,)) to cache["K"] and cache["V"]
    (lists), then attend from q over every cached position. Return the output (d,)."""
    raise NotImplementedError
