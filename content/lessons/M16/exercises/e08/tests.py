import math
import sub


def test_mvt():
    c = sub.mean_value_point(lambda x: x ** 3, lambda x: 3 * x * x, 0.0, 2.0)
    assert abs(c - 2 / math.sqrt(3)) < 1e-10
    c = sub.mean_value_point(math.exp, math.exp, 0.0, 1.0)
    assert abs(c - math.log(math.e - 1)) < 1e-10


def test_remainder_point_between():
    for x in (0.1, 1.0, 3.0, -2.0):
        xi = sub.taylor_remainder_point(x)
        assert min(0, x) < xi < max(0, x)
        assert abs(math.exp(x) - 1 - x - math.exp(xi) * x * x / 2) < 1e-12 * max(1, math.exp(x))
