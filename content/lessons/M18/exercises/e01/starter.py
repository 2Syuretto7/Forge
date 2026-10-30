import numpy as np


# provided
def f1(v):
    x, y = v
    return x * x * y + np.sin(y)


def grad_f1(v):
    """Gradient of x^2 y + sin y."""
    raise NotImplementedError


def grad_f2(x):
    """Gradient of |x|^2."""
    raise NotImplementedError


def grad_f3(x):
    """Gradient of log-sum-exp: the softmax."""
    raise NotImplementedError


def grad_f4(x, A):
    """Gradient of x^T A x / 2."""
    raise NotImplementedError
