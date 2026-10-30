import numpy as np


def rayleigh(S, x):
    """x^T S x / x^T x."""
    return float(x @ S @ x / (x @ x))


def rayleigh_grad(S, x):
    """Gradient of the Rayleigh quotient."""
    return 2.0 / (x @ x) * (S @ x - rayleigh(S, x) * x)


def ascend(S, x0, lr, steps):
    """Gradient ascent with renormalization."""
    x = x0 / np.linalg.norm(x0)
    for _ in range(steps):
        x = x + lr * rayleigh_grad(S, x)
        x = x / np.linalg.norm(x)
    return x
