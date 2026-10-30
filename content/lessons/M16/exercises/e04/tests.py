import math
import sub


def test_root():
    r, h = sub.secant(lambda x: math.cos(x) - x, 0.0, 1.0)
    assert abs(math.cos(r) - r) < 1e-14


def test_superlinear_order():
    r = 0.7390851332151607
    _, h = sub.secant(lambda x: math.cos(x) - x, 0.0, 1.0)
    p = sub.order_estimates([abs(x - r) for x in h])
    assert p, "some errors should fall in the usable range"
    assert 1.4 < p[-1] < 1.85, p
