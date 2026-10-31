import numpy as np
import time


def row_norms_loop(X):
    """Euclidean norm of every row, one Python-level operation per element."""
    out = np.zeros(X.shape[0])
    for i in range(X.shape[0]):
        s = 0.0
        for j in range(X.shape[1]):
            s += X[i, j] * X[i, j]
        out[i] = s ** 0.5
    return out


def row_norms_vector(X):
    """The same in one vectorized call."""
    return np.sqrt((X * X).sum(axis=1))


def time_per_call(f, X, min_time=0.02):
    """Seconds per call of f(X): call it 1, 2, 4, ... times in a row until one batch of calls takes
    at least min_time, then divide that batch's time by its number of calls."""
    n = 1
    while True:
        t = time.perf_counter()
        for _ in range(n):
            f(X)
        elapsed = time.perf_counter() - t
        if elapsed >= min_time:
            return elapsed / n
        n *= 2


def overhead_ratio(rows=200, cols=100, repeats=3):
    """Best-of-repeats time per call of the loop version divided by that of the vectorized version."""
    X = np.random.default_rng(0).normal(size=(rows, cols))
    best = lambda f: min(time_per_call(f, X) for _ in range(repeats))
    return best(row_norms_loop) / best(row_norms_vector)
