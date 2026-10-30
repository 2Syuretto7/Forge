import math


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


def derivative(f, x):
    return f(Dual(x, 1.0)).eps
