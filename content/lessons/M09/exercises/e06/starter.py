import numpy as np


def normalize_rows(X):
    """Each row divided by its length."""
    raise NotImplementedError


def cosine_matrix(X):
    """(n, n) cosine similarities between rows."""
    raise NotImplementedError


def most_similar_pair(X):
    """(i, j), i < j, with the largest cosine."""
    raise NotImplementedError
