import numpy as np


def anisotropic(n, d, common, rng):
    """Rows sharing a common component of length common * sqrt(d)."""
    raise NotImplementedError


def mean_pairwise_cosine(X):
    """Average cosine over all pairs of rows."""
    raise NotImplementedError


def center(X):
    """Subtract the mean row."""
    raise NotImplementedError


def predicted_cosine(common):
    """Typical cosine between rows with a shared component."""
    raise NotImplementedError
