import numpy as np


def scalar_condition(f, df, x):
    """Relative condition number of f at x."""
    return abs(x * df(x) / f(x))


def hilbert(n):
    """The n by n Hilbert matrix."""
    return 1.0 / (np.add.outer(np.arange(n), np.arange(n)) + 1)


def matrix_condition(A):
    """2-norm condition number."""
    s = np.linalg.svd(A, compute_uv=False)
    return float(s[0] / s[-1])


def solve_error(n):
    """(relative error of solving H x = H 1, condition number of H)."""
    H = hilbert(n)
    x = np.linalg.solve(H, H @ np.ones(n))
    return float(np.linalg.norm(x - 1) / np.sqrt(n)), matrix_condition(H)
