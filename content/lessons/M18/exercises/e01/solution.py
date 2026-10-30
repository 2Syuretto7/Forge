import numpy as np


# provided
def f1(v):
    x, y = v
    return x * x * y + np.sin(y)


def grad_f1(v):
    """Gradient of x^2 y + sin y."""
    x, y = v
    return np.array([2 * x * y, x * x + np.cos(y)])


def grad_f2(x):
    """Gradient of |x|^2."""
    return 2 * np.asarray(x, dtype=float)


def grad_f3(x):
    """Gradient of log-sum-exp: the softmax."""
    z = np.exp(x - np.max(x))
    return z / z.sum()


def grad_f4(x, A):
    """Gradient of x^T A x / 2."""
    return 0.5 * (A + A.T) @ x
