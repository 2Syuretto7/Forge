import numpy as np


def unbroadcast(g, shape):
    """Sum g over the axes that broadcasting added or stretched, to get `shape`."""
    while g.ndim > len(shape):
        g = g.sum(axis=0)
    for i, s in enumerate(shape):
        if s == 1 and g.shape[i] != 1:
            g = g.sum(axis=i, keepdims=True)
    return g
