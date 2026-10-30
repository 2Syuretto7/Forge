import numpy as np


def accumulate(chunks):
    """(sum of A^T A, sum of A^T b) over chunks."""
    raise NotImplementedError


def stream_fit(chunks):
    """Least squares from accumulated normal equations."""
    raise NotImplementedError


def make_chunks(n_rows, n_cols, chunk, seed=0):
    """Yield (A, b) chunks of a synthetic regression problem."""
    raise NotImplementedError
