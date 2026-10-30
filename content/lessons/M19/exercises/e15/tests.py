import math
import sub


def build():
    x, w, y = sub.Var(0.7), sub.Var(1.5), sub.Var(1.3)
    z = x * w
    f = sub.sin(sub.sin(sub.sin(z))) + z * y
    return x, y, f


def exact_dx(x, w, y):
    z = x * w
    return (math.cos(math.sin(math.sin(z))) * math.cos(math.sin(z)) * math.cos(z) + y) * w


def test_topological_order_is_right():
    x, y, f = build()
    sub.backward_in(f, sub.reverse_topo_order(f))
    assert abs(x.grad - exact_dx(0.7, 1.5, 1.3)) < 1e-12 and abs(y.grad - 1.05) < 1e-12


def test_bfs_order_is_wrong():
    x, y, f = build()
    sub.backward_in(f, sub.bfs_order(f))
    assert abs(x.grad - exact_dx(0.7, 1.5, 1.3)) > 0.1
