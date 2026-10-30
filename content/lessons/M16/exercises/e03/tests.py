import math
import sub


def test_sqrt():
    for a in (2.0, 10.0, 0.01, 1e10):
        assert abs(sub.newton_sqrt(a) - math.sqrt(a)) <= 1e-15 * math.sqrt(a) * 4


def test_quadratic_convergence():
    _, h = sub.newton(lambda x: x * x - 2, lambda x: 2 * x, 1.0)
    e = [abs(x - math.sqrt(2)) for x in h]
    assert abs(e[3] / e[2] ** 2 - 1 / (2 * math.sqrt(2))) < 0.01
    assert e[4] < 1e-11


def test_zero_derivative():
    try:
        sub.newton(lambda x: x * x + 1, lambda x: 2 * x, 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("expected ValueError")
