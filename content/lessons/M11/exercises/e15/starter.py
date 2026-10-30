import numpy as np


def system(delta):
    """(A, b) for the nearly repeated sensors."""
    raise NotImplementedError


def amplification(delta, db):
    """|change in x| / |change in the second reading|."""
    raise NotImplementedError


def cond_inf(A):
    """||A|| ||A^-1|| in the infinity norm."""
    raise NotImplementedError
