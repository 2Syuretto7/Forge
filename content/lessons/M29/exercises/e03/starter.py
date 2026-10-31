import numpy as np


def heavy_ball(A, b, x0, alpha, beta, iters):
    """Error norms of heavy-ball momentum on (1/2) x^T A x - b^T x."""
    raise NotImplementedError


def optimal_heavy_ball(L, mu):
    """Optimal step and momentum for a quadratic."""
    raise NotImplementedError
