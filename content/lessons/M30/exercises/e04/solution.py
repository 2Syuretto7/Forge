import numpy as np


def _x_of(Q, c, A, lam):
    return -np.linalg.solve(Q, c + A.T @ lam)


def primal_value(Q, c, x):
    """(1/2) x^T Q x + c^T x."""
    return float(0.5 * x @ Q @ x + c @ x)


def dual_value(Q, c, A, b, lam):
    """The dual function at lam."""
    v = c + A.T @ lam
    return float(-0.5 * v @ np.linalg.solve(Q, v) - b @ lam)


def dual_grad(Q, c, A, b, lam):
    """Gradient of the dual function: A x(lam) - b."""
    return A @ _x_of(Q, c, A, lam) - b


def dual_ascent(Q, c, A, b, step, iters):
    """Projected gradient ascent on the dual; returns (lam, x(lam))."""
    lam = np.zeros(len(b))
    for _ in range(iters):
        lam = np.maximum(lam + step * dual_grad(Q, c, A, b, lam), 0)
    return lam, _x_of(Q, c, A, lam)
