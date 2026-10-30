import math
from collections import deque


# provided
class Var:
    def __init__(self, value, parents=()):
        self.value = float(value)
        self.grad = 0.0
        self.parents = parents

    def __add__(self, o):
        return Var(self.value + o.value, ((self, 1.0), (o, 1.0)))

    def __mul__(self, o):
        return Var(self.value * o.value, ((self, o.value), (o, self.value)))


# provided
def sin(x):
    return Var(math.sin(x.value), ((x, math.cos(x.value)),))


def backward_in(out, order):
    """Backward pass in the given processing order."""
    out.grad = 1.0
    for v in order:
        for p, local in v.parents:
            p.grad += v.grad * local


def bfs_order(out):
    """Breadth-first from out, each node once."""
    order, seen, q = [], {id(out)}, deque([out])
    while q:
        v = q.popleft()
        order.append(v)
        for p, _ in v.parents:
            if id(p) not in seen:
                seen.add(id(p))
                q.append(p)
    return order


def reverse_topo_order(out):
    """Reverse of a depth-first postorder."""
    order, seen = [], set()

    def visit(v):
        if id(v) in seen:
            return
        seen.add(id(v))
        for p, _ in v.parents:
            visit(p)
        order.append(v)

    visit(out)
    return order[::-1]
