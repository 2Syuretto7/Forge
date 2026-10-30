import numpy as np


def naive_cosine(x, y):
    """x . y / (|x| |y|), nan for a zero vector."""
    raise NotImplementedError


def safe_cosine(x, y, eps=1e-12):
    """Cosine, or ValueError if either vector is (nearly) zero."""
    raise NotImplementedError


def normalize_rows_safe(X, eps=1e-12):
    """(normalized rows with tiny rows left at zero, indices of the tiny rows)."""
    raise NotImplementedError
