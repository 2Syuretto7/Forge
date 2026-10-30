import math
import sub


def central(f, xs, i, h=1e-6):
    a, b = list(xs), list(xs)
    a[i] += h
    b[i] -= h
    return (f(*a) - f(*b)) / (2 * h)


def run(f, xs):
    vs = [sub.Var(x) for x in xs]
    out = f(*vs)
    sub.backward(out)
    return out.value, [v.grad for v in vs]


def test_grad_simple():
    val, g = run(lambda x, y: x * y + sub.sin(x), [2.0, 3.0])
    assert abs(val - (6 + math.sin(2))) < 1e-15
    assert abs(g[0] - (3 + math.cos(2))) < 1e-12 and abs(g[1] - 2) < 1e-12


def test_grad_reuse_and_composition():
    fv = lambda x, y: sub.tanh(x * x / (1 + y ** 2)) + sub.exp(-x) * sub.log(y) - x  # noqa: E731
    ff = lambda x, y: math.tanh(x * x / (1 + y ** 2)) + math.exp(-x) * math.log(y) - x  # noqa: E731
    for xs in ([0.7, 1.3], [-1.1, 2.4], [2.0, 0.6]):
        _, g = run(fv, xs)
        for i in range(2):
            assert abs(g[i] - central(ff, xs, i)) < 1e-8


def test_x_times_x():
    _, g = run(lambda x: x * x, [3.0])
    assert g == [6.0]
