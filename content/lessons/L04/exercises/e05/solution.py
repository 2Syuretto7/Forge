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

    def __repr__(self):
        return f"Tensor(shape={self.data.shape}, op={self.op!r})"

    def _accumulate(self, g):
        self.grad = g.copy() if self.grad is None else self.grad + g

    def __add__(self, other):
        other = as_tensor(other)
        out = Tensor(self.data + other.data, (self, other), "add")

        def _backward():
            self._accumulate(unbroadcast(out.grad, self.shape))
            other._accumulate(unbroadcast(out.grad, other.shape))
        out._backward = _backward
        return out

    __radd__ = __add__

    def __mul__(self, other):
        other = as_tensor(other)
        out = Tensor(self.data * other.data, (self, other), "mul")

        def _backward():
            self._accumulate(unbroadcast(out.grad * other.data, self.shape))
            other._accumulate(unbroadcast(out.grad * self.data, other.shape))
        out._backward = _backward
        return out

    __rmul__ = __mul__

    def sum(self, axis=None, keepdims=False):
        out = Tensor(self.data.sum(axis=axis, keepdims=keepdims), (self,), "sum")

        def _backward():
            g = out.grad
            if axis is not None and not keepdims:
                g = np.expand_dims(g, axis)
            self._accumulate(np.broadcast_to(g, self.shape).copy())
        out._backward = _backward
        return out

    def backward(self):
        order, seen, stack = [], set(), [(self, False)]
        while stack:
            node, done = stack.pop()
            if done:
                order.append(node)
                continue
            if id(node) in seen:
                continue
            seen.add(id(node))
            stack.append((node, True))
            for p in node._parents:
                if id(p) not in seen:
                    stack.append((p, False))
        for node in order:
            if node._parents:
                node.grad = None  # intermediate gradients do not persist between passes
        self.grad = np.ones_like(self.data)
        for node in reversed(order):
            if node._backward is not None and node.grad is not None:
                node._backward()


def _matmul(self, other):
    other = as_tensor(other)
    out = Tensor(self.data @ other.data, (self, other), "matmul")

    def _backward():
        self._accumulate(out.grad @ other.data.T)
        other._accumulate(self.data.T @ out.grad)
    out._backward = _backward
    return out


def _transpose(self):
    out = Tensor(self.data.T, (self,), "transpose")

    def _backward():
        self._accumulate(out.grad.T)
    out._backward = _backward
    return out


def _reshape(self, *shape):
    out = Tensor(self.data.reshape(*shape), (self,), "reshape")

    def _backward():
        self._accumulate(out.grad.reshape(self.shape))
    out._backward = _backward
    return out


Tensor.__matmul__ = _matmul
Tensor.T = property(_transpose)
Tensor.reshape = _reshape
