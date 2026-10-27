import numpy as np


def rayleigh(S, x):
    """Return x^T S x / x^T x as a float."""
    return float(x @ S @ x / (x @ x))


def rayleigh_grad(S, x):
    """Return the gradient of the Rayleigh quotient at x, shape (n,)."""
    return 2.0 / (x @ x) * (S @ x - rayleigh(S, x) * x)


def ascend(S, x0, lr, steps):
    """Gradient ascent with renormalization. Return a unit vector (n,)."""
    x = x0 / np.linalg.norm(x0)
    for _ in range(steps):
        x = x + lr * rayleigh_grad(S, x)
        x = x / np.linalg.norm(x)
    return x
