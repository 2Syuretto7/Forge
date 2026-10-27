import numpy as np


def cond2(A):
    """Return sigma_max / sigma_min for square A."""
    raise NotImplementedError


def amplification(A, b, db):
    """Return (|dx| / |x|) / (|db| / |b|) for A x = b and A dx = db."""
    raise NotImplementedError


def worst_case_pair(A):
    """Return unit vectors (b, db) whose amplification equals cond2(A)."""
    raise NotImplementedError
