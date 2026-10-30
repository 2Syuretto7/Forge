import numpy as np


def build_index(X):
    """Normalized rows, float32."""
    raise NotImplementedError


def batch_search(index, Q, k):
    """(len(Q), k) top-k indices for every query, from one matrix product."""
    raise NotImplementedError


def flops_per_query(n, d):
    """2 n d."""
    raise NotImplementedError
