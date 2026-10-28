import numpy as np
import time


def row_norms_loop(X):
    """Euclidean norm of every row, one Python-level operation per element."""
    raise NotImplementedError


def row_norms_vector(X):
    """The same in one vectorized call."""
    raise NotImplementedError


def overhead_ratio(rows=200, cols=100, repeats=3):
    """Best-of-repeats time of the loop version divided by that of the vectorized version."""
    raise NotImplementedError
