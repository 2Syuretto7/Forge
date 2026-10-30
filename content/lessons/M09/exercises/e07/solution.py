import numpy as np


def top_k(query, X, k):
    """Indices of the k rows most cosine-similar to query, best first."""
    s = (X @ query) / (np.linalg.norm(X, axis=1) * np.linalg.norm(query))
    return [int(i) for i in np.argsort(-s, kind="stable")[:k]]


def top_k_euclidean(query, X, k):
    """Indices of the k nearest rows in Euclidean distance."""
    d = np.linalg.norm(X - query, axis=1)
    return [int(i) for i in np.argsort(d, kind="stable")[:k]]


def same_order_when_normalized(query, X, k):
    """Whether cosine and Euclidean top-k agree for normalized vectors."""
    U = X / np.linalg.norm(X, axis=1, keepdims=True)
    q = query / np.linalg.norm(query)
    return top_k(q, U, k) == top_k_euclidean(q, U, k)
