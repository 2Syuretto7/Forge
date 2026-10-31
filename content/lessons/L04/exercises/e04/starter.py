import numpy as np


def unbroadcast(g, shape):
    """Sum g over the axes that broadcasting added or stretched, to get `shape`."""
    while g.ndim > len(shape):
        g = g.sum(axis=0)
    for i, s in enumerate(shape):
        if s == 1 and g.shape[i] != 1:
            g = g.sum(axis=i, keepdims=True)
    return g


def as_tensor(x):
    return x if isinstance(x, Tensor) else Tensor(x)


class Tensor:
    def __init__(self, data, parents=(), op=""):
        self.data = np.array(data, dtype=float)
        self.grad = None
        self._parents = parents
        self._backward = None
        self.op = op

    @property
    def shape(self):
        return self.data.shape

    def _accumulate(self, g):
        self.grad = g.copy() if self.grad is None else self.grad + g

    def __add__(self, other):
        raise NotImplementedError

    __radd__ = __add__

    def __mul__(self, other):
        raise NotImplementedError

    __rmul__ = __mul__

    def sum(self, axis=None, keepdims=False):
        raise NotImplementedError

    def backward(self):
        raise NotImplementedError
