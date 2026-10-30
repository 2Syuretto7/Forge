import math
import sub


def test_grad_second_difference():
    for f, d2, x in [(math.exp, math.exp, 0.5), (math.sin, lambda t: -math.sin(t), 1.2), (lambda t: t ** 4, lambda t: 12 * t * t, 0.7)]:
        assert abs(sub.second_diff(f, x) - d2(x)) < 1e-5


def test_convexity_agrees():
    cases = [
        (lambda x: x * x, -2, 2, True),
        (math.exp, -1, 3, True),
        (lambda x: math.exp(x) - 2 * x, -1, 3, True),
        (math.sin, 0, math.pi, False),
        (math.sin, math.pi, 2 * math.pi, True),
        (lambda x: x ** 3, -1, 1, False),
    ]
    for f, a, b, convex in cases:
        assert sub.convex_on_grid(f, a, b) == convex
        assert sub.chord_check(f, a, b) == convex
