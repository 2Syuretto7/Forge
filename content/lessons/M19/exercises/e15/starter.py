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
    raise NotImplementedError


def bfs_order(out):
    """Breadth-first from out, each node once."""
    raise NotImplementedError


def reverse_topo_order(out):
    """Reverse of a depth-first postorder."""
    raise NotImplementedError
