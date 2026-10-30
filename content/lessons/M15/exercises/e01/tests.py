import math
import random
import sub

X = ("x",)
C = lambda v: ("c", v)  # noqa: E731
EXPRS = [
    ("^", X, 3),
    ("*", ("sin", X), ("exp", X)),
    ("sin", ("^", X, 2)),
    ("+", ("*", C(3.0), ("cos", X)), ("^", ("+", X, C(1.0)), 4)),
    ("exp", ("sin", ("*", C(2.0), X))),
]


def central(e, x, h=1e-5):
    return (sub.evaluate(e, x + h) - sub.evaluate(e, x - h)) / (2 * h)


def test_evaluate():
    assert sub.evaluate(EXPRS[0], 2.0) == 8.0
    assert abs(sub.evaluate(EXPRS[1], 1.0) - math.sin(1) * math.e) < 1e-15


def test_grad_symbolic_matches_central_differences():
    rnd = random.Random(0)
    for e in EXPRS:
        d = sub.derivative(e)
        for _ in range(20):
            x = rnd.uniform(-2, 2)
            exact, approx = sub.evaluate(d, x), central(e, x)
            assert abs(exact - approx) <= 1e-6 * max(1, abs(exact)), (e, x, exact, approx)


def test_size_grows():
    e = ("sin", ("sin", ("sin", X)))
    assert sub.size(e) == 4
    assert sub.size(sub.derivative(sub.derivative(e))) > 3 * sub.size(sub.derivative(e))
