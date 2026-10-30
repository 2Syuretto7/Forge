import numpy as np


def build_index(X):
    """Normalized rows, float32."""
    return (X / np.linalg.norm(X, axis=1, keepdims=True)).astype(np.float32)


def batch_search(index, Q, k):
    """(len(Q), k) top-k indices for every query, from one matrix product."""
    Qn = Q / np.linalg.norm(Q, axis=1, keepdims=True)
    S = Qn.astype(np.float32) @ index.T
    idx = np.argpartition(-S, k, axis=1)[:, :k]
    order = np.argsort(-np.take_along_axis(S, idx, axis=1), axis=1)
    return np.take_along_axis(idx, order, axis=1)


def flops_per_query(n, d):
    """2 n d."""
    return 2 * n * d
