import numpy as np


def top_k(query, X, k):
    """Indices of the k rows most cosine-similar to query, best first."""
    raise NotImplementedError


def top_k_euclidean(query, X, k):
    """Indices of the k nearest rows in Euclidean distance."""
    raise NotImplementedError


def same_order_when_normalized(query, X, k):
    """Whether cosine and Euclidean top-k agree for normalized vectors."""
    raise NotImplementedError
