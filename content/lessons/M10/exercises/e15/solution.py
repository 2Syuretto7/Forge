import numpy as np


def broadcast_shape(s1, s2):
    """NumPy's broadcasting rule."""
    n = max(len(s1), len(s2))
    a = (1,) * (n - len(s1)) + tuple(s1)
    b = (1,) * (n - len(s2)) + tuple(s2)
    out = []
    for x, y in zip(a, b):
        if x != y and 1 not in (x, y):
            raise ValueError(f"cannot broadcast {s1} with {s2}")
        out.append(y if x == 1 else x)
    return tuple(out)


def strict_sub(a, b):
    """a - b only for identical shapes."""
    if np.shape(a) != np.shape(b):
        raise ValueError(f"shapes differ: {np.shape(a)} and {np.shape(b)}")
    return a - b


def mse(pred, target):
    """Mean squared error with a shape check."""
    d = strict_sub(pred, target)
    return float(np.mean(d * d))
