import numpy as np


def loss(x, A, b):
    """Return ||Ax - b||^2 as a float."""
    r = A @ x - b
    return float(r @ r)


def grad(x, A, b):
    """Return the gradient of the loss with respect to x, shape (n,)."""
    return 2.0 * A.T @ (A @ x - b)


def gd_solve(A, b, steps):
    """Gradient descent from x = 0 with step 1 / (2 * sigma_max^2). Return x (n,)."""
    eta = 1.0 / (2.0 * np.linalg.norm(A, 2) ** 2)
    x = np.zeros(A.shape[1])
    for _ in range(steps):
        x = x - eta * grad(x, A, b)
    return x
