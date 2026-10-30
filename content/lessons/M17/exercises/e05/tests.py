import math
import sub

PAIRS = [
    (sub.F1, lambda x: x * math.exp(x)),
    (sub.F2, math.log),
    (sub.F3, lambda x: x * math.sin(x)),
    (sub.F4, lambda x: 2 * x / (1 + x * x)),
    (sub.F5, lambda x: math.cos(x) * math.exp(math.sin(x))),
]


def simpson(f, a, b, n=200):
    h = (b - a) / n
    return h / 3 * sum((1 if k in (0, n) else 4 if k % 2 else 2) * f(a + k * h) for k in range(n + 1))


def test_grad_antiderivatives():
    h = 1e-5
    for F, f in PAIRS:
        for x in (0.3, 1.1, 2.4):
            assert abs((F(x + h) - F(x - h)) / (2 * h) - f(x)) < 1e-7


def test_definite():
    for F, f in PAIRS:
        assert abs(sub.definite(F, 0.5, 2.0) - simpson(f, 0.5, 2.0)) < 1e-8
    assert abs(sub.definite(sub.F1, 0, 1) - 1) < 1e-15
