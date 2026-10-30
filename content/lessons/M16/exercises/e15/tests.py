import math
import sub


def test_grad_derivatives():
    h = 1e-6
    for x in (-1.3, 0.3, 2.0):
        assert abs(sub.df(x) - (sub.f(x + h) - sub.f(x - h)) / (2 * h)) < 1e-8
        assert abs(sub.d2f(x) - (sub.df(x + h) - sub.df(x - h)) / (2 * h)) < 1e-8


def test_plain_newton_finds_the_maximum():
    x = sub.newton_min(sub.df, sub.d2f, 0.3)
    assert abs(x) < 1e-12 and sub.d2f(x) < 0


def test_safe_newton_finds_a_minimum():
    x = sub.safe_newton_min(sub.df, sub.d2f, 0.3)
    assert abs(abs(x) - math.sqrt(2)) < 1e-12 and sub.d2f(x) > 0
