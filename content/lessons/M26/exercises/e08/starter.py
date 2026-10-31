import numpy as np


def naive_sum32(x):
    """Sequential float32 sum."""
    raise NotImplementedError


def pairwise_sum32(x):
    """Pairwise float32 sum."""
    raise NotImplementedError


def _kahan_rows(rows):
    raise NotImplementedError


def kahan_sum32(x, width=10000):
    """Kahan float32 sum, vectorized across width running sums."""
    raise NotImplementedError
