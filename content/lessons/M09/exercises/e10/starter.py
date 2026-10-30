import time

import numpy as np


def make_database(n, d, seed=0):
    """n random float32 vectors of length d."""
    raise NotImplementedError


def _normalized(X):
    raise NotImplementedError


def search_loop(query, X, k):
    """Top-k cosine indices with a Python loop over rows."""
    raise NotImplementedError


def search_vectorized(query, X, k):
    """Top-k cosine indices with one matrix-vector product."""
    raise NotImplementedError


def speedup(n, d, k=5):
    """Time of the loop search over time of the vectorized search."""
    raise NotImplementedError
