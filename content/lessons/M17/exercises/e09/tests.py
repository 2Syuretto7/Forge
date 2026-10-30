import math
import sub


def test_spectacular_trapezoid():
    assert abs(sub.gauss_trapezoid(40) - math.sqrt(math.pi)) < 1e-13
    assert abs(sub.gauss_trapezoid(10) - math.sqrt(math.pi)) > 1e-6


def test_squared():
    a, b = sub.squared_check(1000)
    assert abs(a - math.pi) < 1e-12 and abs(b - math.pi) < 1e-9
