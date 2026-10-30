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
    order, seen = [], set()

    def visit(v):
        if id(v) in seen:
            return
        seen.add(id(v))
        for p, _ in v.parents:
            visit(p)
        order.append(v)

    visit(out)
    return order


def is_valid_order(order):
    """Whether each node follows its parents."""
    pos = {id(v): i for i, v in enumerate(order)}
    return all(pos[id(p)] < pos[id(v)] for v in order for p, _ in v.parents if id(p) in pos)


def count_paths(out, leaf):
    """Number of paths from out down to leaf."""
    memo = {}

    def paths(v):
        if v is leaf:
            return 1
        if id(v) not in memo:
            memo[id(v)] = sum(paths(p) for p, _ in v.parents)
        return memo[id(v)]

    return paths(out)
