import numpy as np


def bce_with_logits(a, y):
    a = np.asarray(a, dtype=float)
    y = np.asarray(y, dtype=float)
    return np.maximum(a, 0) - a * y + np.log1p(np.exp(-np.abs(a)))


def bce_grad(a, y):
    a = np.asarray(a, dtype=float)
    return 1.0 / (1.0 + np.exp(-a)) - np.asarray(y, dtype=float)


def binary_entropy(p):
    p = float(p)
    out = 0.0
    for v in (p, 1 - p):
        if v > 0:
            out -= v * np.log(v)
    return out
