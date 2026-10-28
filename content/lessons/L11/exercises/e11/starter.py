import numpy as np
import time


def row_norms_loop(X):
    """Euclidean norm of every row, one Python-level operation per element."""
    raise NotImplementedError


def row_norms_vector(X):
    """The same in one vectorized call."""
    raise NotImplementedError


def time_per_call(f, X, min_time=0.02):
    """Seconds per call of f(X): call it 1, 2, 4, ... times in a row until one batch of calls takes
    at least min_time, then divide that batch's time by its number of calls."""
    raise NotImplementedError


def overhead_ratio(rows=200, cols=100, repeats=3):
    """Best-of-repeats time per call of the loop version divided by that of the vectorized version."""
    raise NotImplementedError
