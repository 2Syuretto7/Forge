import math
import sub


def test_hat():
    assert [sub.hat(x) for x in [-1, 0, 0.5, 1, 1.5, 2, 3]] == [0, 0, 0.5, 1, 0.5, 0, 0]


def test_relu_sum():
    assert sub.relu_sum(2, 1, 0.5, [1], [2]) == 1 + 1 + 2


def test_interpolant_hits_the_corners():
    f = lambda x: math.exp(-x * x)
    c, s, knots, w = sub.interpolant(f, -3, 3, 12)
    assert len(knots) == 11 and len(w) == 11
    for j in range(13):
        t = -3 + 6 * j / 12
        assert abs(sub.relu_sum(t, c, s, knots, w) - f(t)) < 1e-12


def test_straight_between_corners():
    f = lambda x: x ** 3
    c, s, knots, w = sub.interpolant(f, 0, 2, 4)
    g = lambda x: sub.relu_sum(x, c, s, knots, w)
    for lo in [0, 0.5, 1, 1.5]:
        mid = lo + 0.25
        assert abs(g(mid) - (g(lo) + g(lo + 0.5)) / 2) < 1e-12
