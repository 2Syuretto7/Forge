import numpy as np


def quad_fg(A, b, x):
    """f(x) = 0.5 x^T A x - b^T x and its gradient, for symmetric A."""
    Ax = A @ x
    return 0.5 * x @ Ax - b @ x, Ax - b


def gd(grad, x0, lr, steps):
    """Gradient descent from x0. Return all iterates, shape (steps + 1, d)."""
    xs = [np.array(x0, dtype=float)]
    for _ in range(steps):
        xs.append(xs[-1] - lr * grad(xs[-1]))
    return np.array(xs)
