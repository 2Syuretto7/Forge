import numpy as np


def relu_sum(x):
    """Sum of max(0, x_i)."""
    return float(np.sum(np.maximum(0.0, x)))


def relu_sum_grad(x):
    """Indicator of positive entries."""
    return (np.asarray(x) > 0).astype(float)


def check_at(x, h=1e-6):
    """Relative error of a central-difference check."""
    x = np.array(x, dtype=float)
    num = np.zeros_like(x)
    for i in range(x.size):
        e = np.zeros_like(x)
        e[i] = h
        num[i] = (relu_sum(x + e) - relu_sum(x - e)) / (2 * h)
    g = relu_sum_grad(x)
    return float(np.linalg.norm(g - num) / max(np.linalg.norm(g) + np.linalg.norm(num), 1e-12))


def safe_point(x, h=1e-6):
    """Move entries near 0 out to +-10h."""
    x = np.asarray(x, dtype=float)
    return np.where(np.abs(x) < 10 * h, np.where(x < 0, -10 * h, 10 * h), x)
