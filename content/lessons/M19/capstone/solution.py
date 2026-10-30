import math

import numpy as np


def _lift(v):
    return v if isinstance(v, Dual) else Dual(v, 0.0)


class Dual:
    """Forward mode: a value and its derivative."""

    def __init__(self, val, eps=0.0):
        self.val = float(val)
        self.eps = float(eps)

    def __add__(self, o):
        o = _lift(o)
        return Dual(self.val + o.val, self.eps + o.eps)

    __radd__ = __add__

    def __sub__(self, o):
        o = _lift(o)
        return Dual(self.val - o.val, self.eps - o.eps)

    def __rsub__(self, o):
        return _lift(o) - self

    def __mul__(self, o):
        o = _lift(o)
        return Dual(self.val * o.val, self.val * o.eps + self.eps * o.val)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = _lift(o)
        return Dual(self.val / o.val, (self.eps * o.val - self.val * o.eps) / (o.val * o.val))

    def __rtruediv__(self, o):
        return _lift(o) / self

    def __neg__(self):
        return Dual(-self.val, -self.eps)

    def __pow__(self, p):
        return Dual(self.val ** p, p * self.val ** (p - 1) * self.eps)

    def __lt__(self, o):
        return self.val < _lift(o).val

    def __gt__(self, o):
        return self.val > _lift(o).val


def _var(v):
    return v if isinstance(v, Var) else Var(v)


class Var:
    """Reverse mode: a value, its parents and an adjoint."""

    def __init__(self, value, parents=()):
        self.value = float(value)
        self.grad = 0.0
        self.parents = parents

    def __add__(self, o):
        o = _var(o)
        return Var(self.value + o.value, ((self, 1.0), (o, 1.0)))

    __radd__ = __add__

    def __sub__(self, o):
        o = _var(o)
        return Var(self.value - o.value, ((self, 1.0), (o, -1.0)))

    def __rsub__(self, o):
        return _var(o) - self

    def __mul__(self, o):
        o = _var(o)
        return Var(self.value * o.value, ((self, o.value), (o, self.value)))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = _var(o)
        return Var(self.value / o.value, ((self, 1 / o.value), (o, -self.value / o.value ** 2)))

    def __rtruediv__(self, o):
        return _var(o) / self

    def __neg__(self):
        return Var(-self.value, ((self, -1.0),))

    def __pow__(self, p):
        return Var(self.value ** p, ((self, p * self.value ** (p - 1)),))

    def __lt__(self, o):
        return self.value < _var(o).value

    def __gt__(self, o):
        return self.value > _var(o).value


def _apply(x, f, df):
    if isinstance(x, Dual):
        return Dual(f(x.val), df(x.val) * x.eps)
    if isinstance(x, Var):
        return Var(f(x.value), ((x, df(x.value)),))
    return f(x)


def exp(x):
    """e^x."""
    return _apply(x, math.exp, math.exp)


def log(x):
    """Natural logarithm."""
    return _apply(x, math.log, lambda v: 1 / v)


def sin(x):
    """Sine."""
    return _apply(x, math.sin, math.cos)


def cos(x):
    """Cosine."""
    return _apply(x, math.cos, lambda v: -math.sin(v))


def tanh(x):
    """Hyperbolic tangent."""
    return _apply(x, math.tanh, lambda v: 1 - math.tanh(v) ** 2)


def sqrt(x):
    """Square root."""
    return _apply(x, math.sqrt, lambda v: 0.5 / math.sqrt(v))


# provided
def target(x):
    a, b, c = x[0], x[1], x[2]
    s = a * b + sin(c)
    t = exp(-s * s / 4)
    u = log(1 + a * a) / (1 + t)
    v = 0
    for k in range(1, 4):
        v = v + (u ** k) / k
    if a > 0:
        w = sqrt(a * a + b * b + 1)
    else:
        w = cos(b) + 2
    y = v * w + tanh(c - a)
    z = y / (1 + b * b) + 3 * t
    return z


def grad_forward(f, x):
    """One dual-number pass per coordinate."""
    n = len(x)
    out = np.zeros(n)
    for j in range(n):
        out[j] = f([Dual(x[i], 1.0 if i == j else 0.0) for i in range(n)]).eps
    return out


def grad_reverse(f, x):
    """One forward evaluation and one backward sweep."""
    vs = [Var(v) for v in x]
    out = f(vs)
    order, seen = [], set()

    def visit(v):
        if id(v) in seen:
            return
        seen.add(id(v))
        for p, _ in v.parents:
            visit(p)
        order.append(v)

    visit(out)
    out.grad = 1.0
    for v in reversed(order):
        for p, local in v.parents:
            p.grad += v.grad * local
    return np.array([v.grad for v in vs])


def fd_grad(f, x, h=1e-6):
    """Central differences on plain floats."""
    x = [float(v) for v in x]
    out = np.zeros(len(x))
    for j in range(len(x)):
        xp, xm = list(x), list(x)
        xp[j] += h
        xm[j] -= h
        out[j] = (f(xp) - f(xm)) / (2 * h)
    return out


def check(f, x):
    """Worst relative error of the exact gradients against central differences."""
    n = fd_grad(f, x)
    rel = lambda g: float(np.linalg.norm(g - n) / (np.linalg.norm(g) + np.linalg.norm(n)))  # noqa: E731
    return max(rel(grad_forward(f, x)), rel(grad_reverse(f, x)))
