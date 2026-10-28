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


def overhead_ratio(rows=200, cols=100, repeats=3):
    """Best-of-repeats time of the loop version divided by that of the vectorized version."""
    X = np.random.default_rng(0).normal(size=(rows, cols))
    def best(f):
        ts = []
        for _ in range(repeats):
            t = time.perf_counter()
            f(X)
            ts.append(time.perf_counter() - t)
        return min(ts)
    return best(row_norms_loop) / best(row_norms_vector)
