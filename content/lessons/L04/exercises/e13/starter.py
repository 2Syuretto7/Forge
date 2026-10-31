def is_grad_enabled():
    raise NotImplementedError


class no_grad:
    """Context manager: operations inside record no parents, so nothing is saved."""

    def __enter__(self):
        raise NotImplementedError

    def __exit__(self, *exc):
        raise NotImplementedError

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
        self._parents = parents if is_grad_enabled() else ()
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
        out._backward = _backward if out._parents else None
        return out

    __radd__ = __add__

    def __mul__(self, other):
        other = as_tensor(other)
        out = Tensor(self.data * other.data, (self, other), "mul")

        def _backward():
            self._accumulate(unbroadcast(out.grad * other.data, self.shape))
            other._accumulate(unbroadcast(out.grad * self.data, other.shape))
        out._backward = _backward if out._parents else None
        return out

    __rmul__ = __mul__

    def sum(self, axis=None, keepdims=False):
        out = Tensor(self.data.sum(axis=axis, keepdims=keepdims), (self,), "sum")

        def _backward():
            g = out.grad
            if axis is not None and not keepdims:
                g = np.expand_dims(g, axis)
            self._accumulate(np.broadcast_to(g, self.shape).copy())
        out._backward = _backward if out._parents else None
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
            if node._backward is not None and node.grad is not None and node._parents:
                node._backward()


def _matmul(self, other):
    other = as_tensor(other)
    out = Tensor(self.data @ other.data, (self, other), "matmul")

    def _backward():
        self._accumulate(out.grad @ other.data.T)
        other._accumulate(self.data.T @ out.grad)
    out._backward = _backward if out._parents else None
    return out


def _transpose(self):
    out = Tensor(self.data.T, (self,), "transpose")

    def _backward():
        self._accumulate(out.grad.T)
    out._backward = _backward if out._parents else None
    return out


def _reshape(self, *shape):
    out = Tensor(self.data.reshape(*shape), (self,), "reshape")

    def _backward():
        self._accumulate(out.grad.reshape(self.shape))
    out._backward = _backward if out._parents else None
    return out


Tensor.__matmul__ = _matmul
Tensor.T = property(_transpose)
Tensor.reshape = _reshape


def _unary(self, value, local, op):
    out = Tensor(value, (self,), op)

    def _backward():
        self._accumulate(out.grad * local())
    out._backward = _backward if out._parents else None
    return out


def _exp(self):
    v = np.exp(self.data)
    return _unary(self, v, lambda: v, "exp")


def _log(self):
    return _unary(self, np.log(self.data), lambda: 1.0 / self.data, "log")


def _relu(self):
    return _unary(self, np.maximum(self.data, 0), lambda: (self.data > 0).astype(float), "relu")


def _tanh(self):
    v = np.tanh(self.data)
    return _unary(self, v, lambda: 1.0 - v ** 2, "tanh")


def _pow(self, p):
    return _unary(self, self.data ** p, lambda: p * self.data ** (p - 1), "pow")


def _neg(self):
    return self * -1.0


def _sub(self, other):
    return self + (-as_tensor(other))


def _rsub(self, other):
    return as_tensor(other) + (-self)


def _div(self, other):
    return self * as_tensor(other) ** -1.0


def _rdiv(self, other):
    return as_tensor(other) * self ** -1.0


def _mean(self, axis=None, keepdims=False):
    n = self.data.size if axis is None else self.data.shape[axis]
    return self.sum(axis=axis, keepdims=keepdims) * (1.0 / n)


Tensor.exp = _exp
Tensor.log = _log
Tensor.relu = _relu
Tensor.tanh = _tanh
Tensor.__pow__ = _pow
Tensor.__neg__ = _neg
Tensor.__sub__ = _sub
Tensor.__rsub__ = _rsub
Tensor.__truediv__ = _div
Tensor.__rtruediv__ = _rdiv
Tensor.mean = _mean


def cross_entropy(logits, y):
    """Mean softmax cross-entropy built from primitive operations."""
    m = Tensor(logits.data.max(axis=1, keepdims=True))  # constant: the loss does not depend on it
    z = logits - m
    lse = z.exp().sum(axis=1, keepdims=True).log()
    onehot = np.eye(logits.shape[1])[y]
    picked = (z * onehot).sum(axis=1, keepdims=True)
    return (lse - picked).mean()


def cross_entropy_fused(logits, y):
    """The same loss as one operation with the backward rule (P - onehot) / B."""
    Z = logits.data - logits.data.max(axis=1, keepdims=True)
    logp = Z - np.log(np.exp(Z).sum(axis=1, keepdims=True))
    B = Z.shape[0]
    out = Tensor(-np.mean(logp[np.arange(B), y]), (logits,), "cross_entropy")

    def _backward():
        P = np.exp(logp)
        P[np.arange(B), y] -= 1.0
        logits._accumulate(out.grad * P / B)
    out._backward = _backward if out._parents else None
    return out


class Module:
    def parameters(self):
        params = []
        for v in self.__dict__.values():
            if isinstance(v, Tensor) and getattr(v, "is_param", False):
                params.append(v)
            elif isinstance(v, Module):
                params.extend(v.parameters())
            elif isinstance(v, (list, tuple)):
                for item in v:
                    if isinstance(item, Module):
                        params.extend(item.parameters())
        return params

    def zero_grad(self):
        for p in self.parameters():
            p.grad = None

    def __call__(self, x):
        return self.forward(x)


def Parameter(data):
    t = Tensor(data)
    t.is_param = True
    return t


class Linear(Module):
    def __init__(self, n_in, n_out, rng):
        self.W = Parameter(rng.normal(size=(n_in, n_out)) * np.sqrt(2.0 / n_in))
        self.b = Parameter(np.zeros(n_out))

    def forward(self, x):
        return x @ self.W + self.b


class MLP(Module):
    def __init__(self, sizes, seed=0):
        rng = np.random.default_rng(seed)
        self.layers = [Linear(a, b, rng) for a, b in zip(sizes, sizes[1:])]

    def forward(self, x):
        for i, layer in enumerate(self.layers):
            x = layer(x)
            if i < len(self.layers) - 1:
                x = x.relu()
        return x


class SGD:
    def __init__(self, params, lr):
        self.params = list(params)
        self.lr = lr

    def step(self):
        for p in self.params:
            if p.grad is not None:
                p.data -= self.lr * p.grad

    def zero_grad(self):
        for p in self.params:
            p.grad = None
