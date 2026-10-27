import math
import numpy as np


def _lift(v):
    return v if isinstance(v, Dual) else Dual(v, 0.0)


class Dual:
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


def _apply(x, f, df):
    if isinstance(x, Dual):
        return Dual(f(x.val), df(x.val) * x.eps)
    return f(x)


def exp(x):
    return _apply(x, math.exp, math.exp)


def log(x):
    return _apply(x, math.log, lambda v: 1.0 / v)


def sin(x):
    return _apply(x, math.sin, math.cos)


def cos(x):
    return _apply(x, math.cos, lambda v: -math.sin(v))


def tanh(x):
    return _apply(x, math.tanh, lambda v: 1.0 - math.tanh(v) ** 2)


def sqrt(x):
    return _apply(x, math.sqrt, lambda v: 0.5 / math.sqrt(v))


def target(x):
    """A 20-line function of three variables. Do not change it."""
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


def grad(f, x):
    """Forward-mode gradient of scalar f at the list of floats x."""
    n = len(x)
    out = np.zeros(n)
    for j in range(n):
        args = [Dual(x[i], 1.0 if i == j else 0.0) for i in range(n)]
        out[j] = f(args).eps
    return out


def fd_grad(f, x, h=1e-6):
    """Central-difference gradient on plain floats."""
    x = [float(v) for v in x]
    out = np.zeros(len(x))
    for j in range(len(x)):
        xp = list(x)
        xm = list(x)
        xp[j] += h
        xm[j] -= h
        out[j] = (f(xp) - f(xm)) / (2 * h)
    return out


def check(f, x):
    """Relative error between grad and fd_grad."""
    g = grad(f, x)
    n = fd_grad(f, x, 1e-6)
    return float(np.linalg.norm(g - n) / (np.linalg.norm(g) + np.linalg.norm(n)))
