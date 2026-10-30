import numpy as np


def loss(x, A, b):
    """||Ax - b||^2."""
    r = A @ x - b
    return float(r @ r)


def slope_vector(x, A, b):
    """s = 2 A^T (Ax - b)."""
    return 2.0 * A.T @ (A @ x - b)


def step_down(A, b, steps):
    """Repeated steps against s with eta = 1 / (2 ||A||_F^2)."""
    eta = 1.0 / (2.0 * np.sum(A * A))
    x = np.zeros(A.shape[1])
    for _ in range(steps):
        x = x - eta * slope_vector(x, A, b)
    return x
