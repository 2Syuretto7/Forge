# provided
class Var:
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

    def __mul__(self, o):
        o = o if isinstance(o, Var) else Var(o)
        return Var(self.value * o.value, ((self, o.value), (o, self.value)))

    __rmul__ = __mul__

    def __truediv__(self, o):
        return Var(self.value / o, ((self, 1 / o),))


# provided
def backward(out):
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


def square_grad(x):
    """d(x * x)/dx through the engine."""
    raise NotImplementedError


def fit_line(xs, ys, steps, lr, zero_grads):
    """Gradient descent on the mean squared error, with or without zeroing."""
    raise NotImplementedError
