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

    def __mul__(self, o):
        o = o if isinstance(o, Var) else Var(o)
        return Var(self.value * o.value, ((self, o.value), (o, self.value)))

    __rmul__ = __mul__


def topo_order(out):
    """Every node after its parents, out last."""
    raise NotImplementedError


def is_valid_order(order):
    """Whether each node follows its parents."""
    raise NotImplementedError


def count_paths(out, leaf):
    """Number of paths from out down to leaf."""
    raise NotImplementedError
