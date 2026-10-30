import numpy as np


def system(delta):
    """(A, b) for the nearly repeated sensors."""
    return np.array([[1.0, 1.0], [1.0, 1.0 + delta]]), np.array([2.0, 2.0 + delta])


def amplification(delta, db):
    """|change in x| / |change in the second reading|."""
    A, b = system(delta)
    x = np.linalg.solve(A, b)
    x2 = np.linalg.solve(A, b + np.array([0.0, db]))
    return float(np.linalg.norm(x2 - x) / abs(db))


def cond_inf(A):
    """||A|| ||A^-1|| in the infinity norm."""
    norm = lambda M: float(np.max(np.sum(np.abs(M), axis=1)))
    return norm(A) * norm(np.linalg.inv(A))
