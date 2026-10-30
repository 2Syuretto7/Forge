import math


class Var:
    """A value with the recipe that produced it."""

    def __init__(self, value, parents=()):
        self.value = float(value)
        self.grad = 0.0
        self.parents = parents

    def __add__(self, o):
        o = o if isinstance(o, Var) else Var(o)
        return Var(self.value + o.value, ((self, 1.0), (o, 1.0)))

    __radd__ = __add__

    def __sub__(self, o):
        o = o if isinstance(o, Var) else Var(o)
        return Var(self.value - o.value, ((self, 1.0), (o, -1.0)))

    def __rsub__(self, o):
        return Var(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, Var) else Var(o)
        return Var(self.value * o.value, ((self, o.value), (o, self.value)))

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = o if isinstance(o, Var) else Var(o)
        return Var(self.value / o.value, ((self, 1 / o.value), (o, -self.value / o.value ** 2)))

    def __rtruediv__(self, o):
        return Var(o) / self

    def __neg__(self):
        return Var(-self.value, ((self, -1.0),))

    def __pow__(self, p):
        return Var(self.value ** p, ((self, p * self.value ** (p - 1)),))


def exp(x):
    """e^x."""
    v = math.exp(x.value)
    return Var(v, ((x, v),))


def log(x):
    """Natural logarithm."""
    return Var(math.log(x.value), ((x, 1 / x.value),))


def sin(x):
    """Sine."""
    return Var(math.sin(x.value), ((x, math.cos(x.value)),))


def tanh(x):
    """Hyperbolic tangent."""
    t = math.tanh(x.value)
    return Var(t, ((x, 1 - t * t),))


def backward(out):
    """Fill .grad of every node with d out / d node."""
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
