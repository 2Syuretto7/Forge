import numpy as np


def directional(grad, x, u):
    """Slope of f in the direction of u."""
    u = np.asarray(u, dtype=float)
    return float(grad(x) @ u / np.linalg.norm(u))


def steepest(grad, x):
    """Unit direction of steepest ascent."""
    g = grad(x)
    return g / np.linalg.norm(g)


def numerical_directional(f, x, u, h=1e-6):
    """Central difference along u."""
    u = np.asarray(u, dtype=float) / np.linalg.norm(u)
    return float((f(x + h * u) - f(x - h * u)) / (2 * h))
