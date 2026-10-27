import math
import sub


def test_arithmetic_rules():
    a = sub.Dual(2.0, 1.0)
    r = (3 * a + 1) * a - a / 4
    assert abs(r.val - (7 * 2 - 0.5)) < 1e-12
    assert abs(r.eps - (6 * 2 + 1 - 0.25)) < 1e-12
    q = 1 / a
    assert abs(q.eps + 0.25) < 1e-12
    s = 5 - a
    assert s.val == 3.0 and s.eps == -1.0
    assert (-a).eps == -1.0


def test_power_and_functions():
    f = lambda x: x ** 3 + sub.exp(2 * x) - sub.log(x)  # noqa: E731
    x = 1.3
    exact = 3 * x ** 2 + 2 * math.exp(2 * x) - 1 / x
    assert abs(sub.derivative(f, x) - exact) < 1e-12


def test_trig_tanh_sqrt():
    f = lambda x: sub.sin(x) * sub.cos(x) + sub.tanh(x) / sub.sqrt(x)  # noqa: E731
    x = 0.8
    t = math.tanh(x)
    exact = math.cos(2 * x) + (1 - t * t) / math.sqrt(x) - 0.5 * t * x ** -1.5
    assert abs(sub.derivative(f, x) - exact) < 1e-12


def test_plain_floats_still_work():
    assert abs(sub.exp(1.0) - math.e) < 1e-15 and isinstance(sub.sin(0.3), float)


def test_branches_follow_the_value():
    def f(x):
        if x > 1.0:
            return x * x
        return 3 * x
    assert sub.derivative(f, 2.0) == 4.0
    assert sub.derivative(f, 0.5) == 3.0
